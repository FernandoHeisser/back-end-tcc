from flask_restx import Resource, fields

from src.config.server.instance import server
from users.users_repository import *

app, api = server.app, server.api

user = api.model('User', {
    '_id': fields.String,
    'stocks': fields.List,
})

@api.route('/users')
@api.expect(user)
class Users(Resource):
    def get(self, ):
        return getUsers()

    def post(self, ):
        return createUser(api.payload)

    def put(self, ):
        return updateUser(api.payload)

@api.route('/users/<string:id>')
class UsersById(Resource):
    def get(self, id):    
        return getUser(id)

    def delete(self, id):    
        return deleteUser(id)

