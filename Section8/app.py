from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import itemList, Items
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
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
