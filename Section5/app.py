from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import itemList, Items

app = Flask(__name__)
api = Api(app)

app.secret_key = 'yoshimitsu'

jwt = JWT(app, authenticate, identity)  # /auth

items = []

api.add_resource(itemList, '/items')
api.add_resource(Items, '/item/<string:name>')
api.add_resource(UserRegister, '/register')  

if __name__ == "__main__":
    app.run(debug=True)
