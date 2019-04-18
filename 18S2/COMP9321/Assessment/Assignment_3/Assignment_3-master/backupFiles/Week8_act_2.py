'''
Description: In this activity you are going implement two methods to encode/decode credential information (username,password) to/from a json/stringself.This will later be used in the 3rd activity
Step:
1, Pick a quite long string (a private key) for encoding and decoding purposes
2, Create a method which accepts a parameter called "username": the method must create a json like {'username':'admin', 'creation_time': XXXXX} then use the itsdangerous's json-web-signatures to encode it into a string with chosen private key
3, Create another method which accepts a token gennerated by the previous step
    it returns the username by decoding the token if it a valid token and if token is created no later than 10 seconds
    otherwise, it returns proper exceptions
4, Create an encrypted token for the valid username and password
5, Decode the token to print the username('admin')
6, wait for 10 seconds and try to decode the token again
7, Create a random string and try to decode it
'''
''' ##### 没看懂这个step 2,3,4 ########
'''
from time import sleep, time
from itsdangerous import JSONWebSignatureSerializer, BadSignature, SignatureExpired

class AuthenticationToken:
    def __init__(self, secret_key, expires_in):
        self.secret_key = secret_key
        self.expires_in = expires_in
        self.serializer = JSONWebSignatureSerializer(secret_key)
    def generate_token(self,username):
        info = 
