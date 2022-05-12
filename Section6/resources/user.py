import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, 
                        required=True, help='Username is required')
    parser.add_argument('password', type=str, 
                        required=True, help='Password is required')
    
    def post(self):
        
        data = self.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': f"User {data['username']} already exists"}, 400
        
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        
        cursor.execute(query, (data['username'], data['password']))
        
        connection.commit()
        connection.close()
        
        return {"message": "User created successfully"}, 201
    