from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
api = Api(app)

app.secret_key = 'yoshimitsu'

jwt = JWT(app, authenticate, identity)  # /auth

items = []

class Items(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True
                            , help="This field cannot be left blank!")
        
    @jwt_required()
    def get(self, name):
        """GET method implementation"""
        
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {'item': item}, 200 if item else 404
    
    def post(self, name):
        """POST method implementation"""
               
        if next(filter(lambda x: x["name"] == name, items), None):
            return {'message': 'Item with name {} already exists'.format(name)}, 400
        
        data = self.parser.parse_args()
        new_item = {"name": name, "price": data['price']}
        items.append(new_item)
        
        return new_item, 201
    
    def delete(self, name):
        
        global items
        
        if next(filter(lambda x: x['name'] == name, items), None):
            items = list(filter(lambda x: x['name'] != name, items))
            return {'message': f'Item {name} deleted'}, 200
        
        return {'message': f'Item {name} does not exist'}, 400
    
    def put(self, name):
              
        item = next(filter(lambda x: x['name'] == name, items), None)
        data = self.parser.parse_args()
        
        if not item:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)       
            
        return item
    
class itemList(Resource):
    
    def get(self):
        """Get item list method"""
        return {"items": items}, 200
    
api.add_resource(itemList, '/items')
api.add_resource(Items, '/item/<string:name>')
api.add_resource(UserRegister, '/register')  

if __name__ == "__main__":
    app.run(debug=True)
