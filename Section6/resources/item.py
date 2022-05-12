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
            new_item.save_to_db()
        except:
            return {'message': "An error occured inserting the item"}, 500  #internal server error
        
        return new_item.json(), 201
    
    def delete(self, name):
        
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            
        return {'message': 'Item deleted'}
    
    def put(self, name):
              
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if not item:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        
        item.save_to_db()
        
        return item.json()

        
class itemList(Resource):
    def get(self):
        """Get item list method"""
        return {'items': [item.json() for item in ItemModel.query.all()]}
    