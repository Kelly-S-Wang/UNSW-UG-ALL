import pymongo

# Connect to mongodb and do operations
class MongoDB:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://cs9321:cs9321@ds261302.mlab.com:61302/kelly-database')
        self.database = self.client['kelly-database']
        self.collection = self.database['cs9321_ass_2']

    def insert_doc(self, data):
        self.collection.insert_one(data)

    def delete_doc(self, query):
        self.collection.delete_one(query)

    def find_all_docs(self):
        return self.collection.find()

    def count_doc(self, query):
        return self.collection.find(query).count()

    def find_doc_1(self, query, fields):
        return self.collection.find_one(query, fields)

    def find_doc_2(self, query):
        return self.collection.find_one(query)

import json
import pandas as pd
from flask import Flask, request
from flask_restplus import Resource, Api, fields, inputs, reqparse
import datetime
import requests
import re
import argparse

app = Flask(__name__)
api = Api(app, default="Indicators", title="World Bank Economics Indicators")


mg = MongoDB()
input_model = api.model('Input', {'indicator': fields.String})


# Q1 & Q3
@api.route('/myCollection')
class WorldBank_Q1_Q3(Resource):

    # Q1 - Import a collection from the data service
    @api.response(200, 'OK')
    @api.response(201, 'Created')
    @api.response(404, 'Requested resource does not exisit')
    @api.doc(description='Q1 - Import a collection from the data service')
    @api.expect(input_model)
    def post(self):

        data = request.json
        id = data['indicator']

        # get the json format data by url
        worldbank_url = f'http://api.worldbank.org/v2/countries/all/indicators/{id}?date=2012:2017&format=json&per_page=2000'
        r = requests.get(worldbank_url)

        data = r.json()

        # Indicator does not exist in the data source
        if (len(data)==1): 
            return {"message": "{} does not exist in the data source".format(id)}, 404

        # The collection has already been imported
        if mg.count_doc({"collection_id": id}):
            return {"message": "{} has already been imported".format(id)}, 200

        # Data which need to import to mlab
        mlab_info = {}
        mlab_info['collection_id'] = data[1][0]['indicator']['id']
        mlab_info['indicator'] = data[1][0]['indicator']['id']
        mlab_info['indicator_value'] = data[1][0]['indicator']['value']
        mlab_info['creation_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mlab_info['entries'] = []

        # Entries list
        for entry in data[1]:
            inDict = {}
            inDict['country'] = entry['country']['value']
            inDict['date'] = entry['date']
            inDict['value'] = entry['value']
            mlab_info['entries'].append(inDict)

        # Import to mlab
        mg.insert_doc(mlab_info)

        # Response message
        resq_info = {}
        resq_info['location'] = "/myCollection/"+mlab_info['collection_id']
        resq_info['collection_id'] = mlab_info['collection_id']
        resq_info['creation_time'] = mlab_info['creation_time']
        resq_info['indicator'] = mlab_info['indicator']

        return resq_info, 201


    # Q3 - Retrieve the list of available collections
    @api.response(200, 'OK')
    @api.doc(description='Q3 - Retrieve the list of available collections')
    def get(self):

        # Response message
        resq_info = []
        for doc in mg.find_all_docs():
            inDict = {}
            inDict['location'] = "/myCollection/"+doc['collection_id']
            inDict['collection_id'] = doc['collection_id']
            inDict['creation_time'] = doc['creation_time']
            inDict['indicator'] = doc['indicator']
            resq_info.append(inDict)

        return resq_info, 200


# Q2 & Q4
@api.route('/myCollection/<string:id>')
@api.doc(params={'id': 'The collection id'})
class WorldBank_Q2_Q4(Resource):

    # Q2 - Deleting a collection with the data service
    @api.response(200, 'OK')
    @api.response(404, 'Requested resource does not exisit')
    @api.doc(description='Q2 - Deleting a collection with the data service')
    def delete(self, id):

        # Indicator does not exist in the data source
        if not mg.count_doc({"collection_id": id}):
            return {"message": "{} does not exist in the data source".format(id)}, 404

        # Delete the collection
        mg.delete_doc({"collection_id": id})

        return {"message": "Collection = {} is removed from the database!".format(id)}, 200

    # Q4 - Retrieve a collection
    @api.response(200, 'OK')
    @api.response(404, 'Requested resource does not exisit')
    @api.doc(description='Q4 - Retrieve a collection')
    def get(self, id):

        # Indicator does not exist in the data source
        if not mg.count_doc({"collection_id": id}):
            return {"message": "{} does not exist in the data source".format(id)}, 404
        
        # Retrieve the collection by collection_id
        resq_info = mg.find_doc_1({"collection_id": id}, {"_id": 0})

        return resq_info, 200


# Q5
@api.route('/myCollection/<string:id>/<int:year>/<string:country>')
@api.doc(params={'id': 'The collection id', 'year': 'The entry date', 'country': 'The entry country'})
class WorldBank_Q5(Resource):

    # Q5 - Retrieve economic indicator value for given country and a year
    @api.response(200, 'OK')
    @api.response(404, 'Requested resource does not exisit')
    @api.doc(description='Q5 - Retrieve economic indicator value for given country and a year')    
    def get(self, id, year, country):

        # Indicator does not exist in the data source
        if not mg.count_doc({"collection_id": id}):
            return {"message": "{} does not exist in the data source".format(id)}, 404

        # Retrieve the collection by collection_id
        res = mg.find_doc_2({"collection_id": id})

        # Sesearch for specific country and year in the collection
        # And change format
        for c in res['entries']:
            if str(c['country']) == country and str(c['date']) == str(year):
                resq_info = {}
                resq_info['collection_id'] = id
                resq_info['indicator'] = res['indicator']
                resq_info['country'] = country
                resq_info['year'] = year
                resq_info['value'] = c['value']
                return resq_info, 200

        # If the specific country and year does not exist in the collection
        return {"message": "{} and/or {} does not exist in {}".format(country, year, id)}, 404 


parser = reqparse.RequestParser()
parser.add_argument('query')

# Q6
@api.route('/myCollection/<string:id>/<int:year>')
@api.doc(params={'id': 'The collection id', 'year': 'The entry date', 'query': 'Get top or bottom info'})
@api.expect(parser)
class WorldBank_Q6(Resource):

    # Q6 - Retrieve top/bottom economic indicator values for a given year
    @api.response(200, 'OK')
    @api.response(400, 'Bad Requested')
    @api.response(404, 'Requested resource does not exisit')
    @api.doc(description='Q6 - Retrieve top/bottom economic indicator values for a given year')
    def get(self, id, year):

        args = parser.parse_args()
        query = args.get('query')

        # id can't be found
        if not mg.count_doc({"collection_id": id}):
            return {"message": "{} does not exist in the data source".format(id)}, 404

        # Retrieve the collection by collection_id
        res = mg.find_doc_2({"collection_id": id})

        # Entries list and change null to -1
        entries = []
        for c in res['entries']:
            if str(c['date']) == str(year):
                if c['value'] == None:
                    c['value'] = -1
                c['value'] = float(c['value'])
                entries.append(c)

        # year can't be found
        if not entries:
            return {"message": "{} does not exist in {}".format(year, id)}, 404

        desc_entries = sorted(entries, key=lambda k: k['value'], reverse=True)
        asec_entries = sorted(entries, key=lambda k: k['value'], reverse=False)

        # Change -1 back to null
        for e in desc_entries:
            if e['value'] == float(-1):
                e['value'] = None

        for e in asec_entries:
            if e['value'] == float(-1):
                e['value'] = None

        # Query is empty, show all results in descending order
        if not query:
            return desc_entries

        # Check if query is valid
        valid_query = re.compile(r'^(top|bottom)\d+$')
        if not re.match(valid_query, query):
            return {"message": "The given query is invalid"}, 400

        # Extract the number in the query
        matches = re.findall(r'\d+', query)
        num = int(matches[0])

        # The number can be an integer value between 1 and 100
        if num > 100 or num < 1:
            return {"message": "The given value for query is invalid"}, 404

        # Response message
        resq = {}
        resq['indicator'] = id
        resq['indicator_value'] = res['indicator_value']

        # Top or bottom
        is_top = query.find('top')
        if is_top == 0:
            resq['entries'] = desc_entries[0:num]
        else:
            resq['entries'] = asec_entries[0:num]

        return resq, 200


if __name__ == '__main__':
    app.run(debug=True)
