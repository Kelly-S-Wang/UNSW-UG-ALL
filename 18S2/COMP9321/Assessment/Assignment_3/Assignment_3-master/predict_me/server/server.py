import pandas as pd
from flask import Flask
from flask import request
from predict import *
from functools import wraps
from time import time
from flask_restplus import Resource, Api, abort
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature
import os, csv, base64, datetime, requests, json


class AuthenticationToken:
    def __init__(self, secret_key, expires_in):
        self.secret_key = secret_key
        self.expires_in = expires_in
        self.active_token = set()

        # encode token using JWS
        self.serializer = JSONWebSignatureSerializer(secret_key)

    def generate_token(self, username):
        info = {
            'username': username,
            'creation_time': time()
        }

        # gnerate a token
        token = self.serializer.dumps(info)

        # >>>>>>> debug
        print(f'token serializer is {token}')
        # <<<<<<< debug

        new_token = token.decode()
        self.active_token.add(new_token)

        # >>>>>>> debug
        print(f'adding new token {new_token}')
        print(f'now active tokens are {self.active_token}')
        # <<<<<<< debug

        return new_token

    def validate_token(self, token):

        # >>>>>>> debug
        print(f'validating token {token}')
        # <<<<<<< debug

        info = self.serializer.loads(token.encode())

        if token not in self.active_token:
            raise SignatureExpired("The Token is no longer active!")
        elif time() - info['creation_time'] > self.expires_in:
            self.active_token.discard(token)

            # >>>>> debug
            print(f'now deleting token {token}')
            print(f'now active tokens are {self.active_token}')
            # <<<<< debug

            raise SignatureExpired("The Token has been expired; get a new token!")
        
        return info['username']

    def delte_token(self, token):
        self.active_token.discard(token)

        # >>>>> debug
        print(f'now deleting token {token}')
        print(f'now active tokens are {self.active_token}')
        # <<<<< debug

        return True


# user account database
class userDatabase:
    def __init__(self):
        self.users = {}

        # load account info from local csv file
        if not os.path.isfile('./userAccounts.csv'):
            with open('userAccounts.csv', 'w', newline='') as csvfile:
                accountWriter = csv.writer(csvfile)
                accountWriter.writerow(['username', 'password'])
        else:
            usr_info_df = pd.read_csv('userAccounts.csv')
            for index, row in usr_info_df.iterrows():
                username, password = row['username'], row['password']
                if username not in self.users:
                    self.users[username] = password

    def save_user(self, username, password):
        self.users.setdefault(username, password)

        # save account info to local csv file
        with open('userAccounts.csv', 'a', newline='') as csvfile:
            accountWriter = csv.writer(csvfile)
            accountWriter.writerow([username, password])
    
    def varifyUser(self, username, password):
        if username in self.users and self.users[username] == password:
            return True
        else:
            return False

    def get_all_users(self):
        return self.users

    def is_in_userDatabase(self, username):
        return username in self.users


# decorator function that authenticate user requests
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get('AUTH-TOKEN')

        # >>>>>>> debug
        print(f'now geting the header token {token}')
        # <<<<<<< debug

        if not token:
            abort(401, 'Authentication token is missing')

        try:
            user = auth.validate_token(token)
        except SignatureExpired as e:
            abort(401, e.message)
        except BadSignature as e:
            abort(401, e.message)

        return f(*args, **kwargs)

    return decorated


# global variables
db = userDatabase()
SECRET_KEY = "Assignment 3 for COMP9321"
expires_in = 1000
auth = AuthenticationToken(SECRET_KEY, expires_in)
app = Flask(__name__)
api = Api(app, authorizations={
                'API-KEY': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'AUTH-TOKEN'
                }
            },
          security='API-KEY',
          default="predict",  # Default namespace
          title="Assignment 3 - Predict Me",  # Documentation Title
          description="Predict Melbourne House Price")  # Documentation Description


credential_model = api.model('credential', {
    'username': fields.String,
    'password': fields.String
})

credential_parser = reqparse.RequestParser()
credential_parser.add_argument('username', type=str)
credential_parser.add_argument('password', type=str)


@api.route('/token')
class Token(Resource):
    @api.response(200, 'Successful')
    @api.response(401, 'Unauthorized')
    @api.doc(description="Generates a authentication token")
    @api.expect(credential_parser, validate=True)
    def get(self):
        global db
        args = credential_parser.parse_args()

        username = args.get('username')
        password = args.get('password')

        # >>>>>> debug
        print(f'The args for requesting token is {args}, username = {username}, password = {password}')
        # <<<<<< debug

        if db.varifyUser(username, password):
            return {"token": auth.generate_token(username)}

        return {"message": "authorization has been refused for those credentials."}, 401


@api.route('/predict/<string:suburb>/<int:size>')
class Preditct (Resource):
    @api.response(200, 'Successful')
    @api.response(401, 'Unauthorized')
    @api.response(400, 'Bad Request')
    @api.doc(description="Machine learning for predicting the house price in Melbourne.")
    @requires_auth
    def get(self, suburb, size):
        if suburb in ['Brunswick', 'Fitzroy North', 'Port Melbourne', 'Reservoir', 'Richmond'] and 0 < size <= 250:
            predicted_price = predict(suburb, size)
            binaryPic = open('./' + suburb + '.png', "rb").read()
            b64Pic = base64.b64encode(binaryPic)
            b64PicString = b64Pic.decode('utf-8')

            return {'predicted_price': predicted_price,
                    'b64PicString': b64PicString}, 200

        else:
            return {"message": "Invalid request data!"}, 400


@api.route('/register')
class Register(Resource):
    @api.response(200, 'Username Already Exists')
    @api.response(201, 'Account Created Successfully')
    @api.response(400, 'Bad Request Error')
    @api.doc(description="Register an account")
    @api.expect(credential_model, validate=True)
    def post(self):
        global db
        
        # >>>>> debug
        print(f'register request is {request}')
        print(f'before request, the urers in database are {db.get_all_users()}')
        # <<<<< debug

        # decode the request into json format
        try:
            accountInfo = request.json
        except:
            return {'message': 'Bad Request!'}, 400
        
        try:
            if db.is_in_userDatabase(accountInfo['username']):
                return {'message': 'Username Already Exists'}, 200

            db.save_user(accountInfo['username'], accountInfo['password'])
            return {'message': 'Account Created Successfully!'}, 201

        except KeyError:
            return {'message': 'Bad Request!'}, 400


@api.route('/signout/<string:token>')
class Signout(Resource):
    @api.response(200, 'Successful')
    @api.doc(description="Signout current user.")
    @requires_auth
    def delete(self, token):
        auth.delte_token(token)
        return {'message': 'Deletion Successful'}, 200







if __name__ == '__main__':

    app.run(host='0.0.0.0', port=12345, debug=True)



