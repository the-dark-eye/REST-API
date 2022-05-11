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
        
        try:
            self.insert(new_item)
        except:
            return {'message': "An error occured inserting the item"}, 500  #internal server error
        
        return new_item, 201
    
    @classmethod
    def insert(cls, new_item):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (new_item['name'], new_item['price']))
        
        connection.commit()        
        connection.close()
    
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
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        
        if not item:
            try:
                self.insert(updated_item)
            except:
                return {'message': "An error occured inserting the item"}, 500
        else:
            try:
                self.update(updated_item)       
            except:
                return {'message': "An error occured updating the item"}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        
        connection.commit()
        connection.close()
        
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