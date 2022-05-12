import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Items(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True
                            , help="This field cannot be left blank!")
        
    @jwt_required()
    def get(self, name):
        """GET method implementation"""
        
        item = ItemModel.find_by_name(name)
        
        if item:
            return item.json(), 200
    
        return {'message': 'Item not found'}, 404
          
    def post(self, name):
        """POST method implementation"""
               
        if ItemModel.find_by_name(name):
            return {'message': 'Item with name {} already exists'.format(name)}, 400
        
        data = self.parser.parse_args()
        new_item = ItemModel(name, data['price'])
        
        try:
            new_item.insert()
        except:
            return {'message': "An error occured inserting the item"}, 500  #internal server error
        
        return new_item.json(), 201
    
    def delete(self, name):
        
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name, ))
        
        connection.commit()
        connection.close()
        
        return {'message': f'Item {name} deleted'}, 200
    
    def put(self, name):
              
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        
        if not item:
            try:
                updated_item.insert()
            except:
                return {'message': "An error occured inserting the item"}, 500
        else:
            try:
                updated_item.update()      
            except:
                return {'message': "An error occured updating the item"}, 500
        return updated_item.json()
        
        
class itemList(Resource):
    
    def get(self):
        """Get item list method"""
        
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        
        items = []
        
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        
        connection.close()
        
        return {'items': items}