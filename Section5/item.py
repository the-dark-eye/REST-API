import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Items(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True
                            , help="This field cannot be left blank!")
        
    @jwt_required()
    def get(self, name):
        """GET method implementation"""
        
        item = self.find_by_name(name)
        
        if item:
            return item, 200
    
        return {'message': 'Item not found'}, 404
        
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        
        connection.close()
        
        if row:
            return {'items': {'name': row[0], 'price': row[1]}}
    
    def post(self, name):
        """POST method implementation"""
               
        if self.find_by_name(name):
            return {'message': 'Item with name {} already exists'.format(name)}, 400
        
        data = self.parser.parse_args()
        new_item = {"name": name, "price": data['price']}
        
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (new_item['name'], new_item['price']))
        
        connection.commit()        
        connection.close()
        
        return new_item, 201
    
    def delete(self, name):
        
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name, ))
        
        connection.commit()
        connection.close()
        
        return {'message': f'Item {name} deleted'}, 200
    
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