import uuid
from flask_restx import Resource, fields

from src.server.instance import server
from src.repositories.UsersRepository import *

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

    def delete(self, ):    
        return deleteUsers()

@api.route('/users/<string:id>')
class UsersById(Resource):
    def get(self, id):    
        user = getUser(id)
        if user is None:
            return "NOT FOUND", 404
        else:
            return user, 200

    def delete(self, id):    
        return deleteUser(id)

@api.route('/session/fetch/<string:id>')
class FetchSession(Resource):
    def get(self, id):
        return fetchUserSession(id)

@api.route('/session/<string:id>')
class GetSession(Resource):
    def get(self, id):    
        return getUserSession(id)
