from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

items = []

class Items(Resource):
    def get(self, name):
        """GET method implementation"""
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {'item': item}, 200 if item else 404
    
    def post(self, name):
        """POST method implementation"""
               
        if next(filter(lambda x: x["name"] == name, items), None):
            return {'message': 'Item with name {} already exists'.format(name)}, 400
        
        post_data = request.get_json()
        new_item = {"name": name, "price": post_data['price']}
        items.append(new_item)
        
        return new_item, 201
        
class itemList(Resource):
    def get(self):
        """Get item list method"""
        return {"items": items}, 200
    
api.add_resource(itemList, '/items')
api.add_resource(Items, '/item/<string:name>')

if __name__ == "__main__":
    app.run(debug=True)
    