import os

from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import itemList, Items
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
con_str = "postgresql://icaqevghwyxxzr:5fc8abb48c4b51dd3c2f64fc8b43eb19b09afc358ad360ee3fad65a761aef6e0@ec2-176-34-211-0.eu-west-1.compute.amazonaws.com:5432/ddjpsnhu7k5d48"
app.config['SQLALCHEMY_DATABASE_URI'] = con_str
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

app.secret_key = 'yoshimitsu'

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(itemList, '/items')
api.add_resource(Items, '/item/<string:name>')
api.add_resource(UserRegister, '/register') 
api.add_resource(Store, '/store/<string:name>') 
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
