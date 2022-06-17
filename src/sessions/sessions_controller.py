from flask_restx import Resource

from src.config.server.instance import server
from src.sessions.sessions_repository import *

app, api = server.app, server.api

@api.route('/session/<string:id>')
class GetSession(Resource):
    def get(self, id):    
        return getSession(id)