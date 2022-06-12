from flask_restx import Resource, fields

from src.server.instance import server
from src.google.news import *

app, api = server.app, server.api

search = api.model('search', {
    'keywords': fields.List,
    'sources': fields.List,
})

#-- Sources ----------------------------------------------

@api.route('/google-news/sources')
class GetGoogleNewsSources(Resource):
    def get(self, ):    
        try:
            sources = list(sourcesDb.find({}))
            response = {
                'size': len(sources),
                'content': sources
            }
            return response
        except:
            print("Error - GetGoogleNewsSources()")
            return "ERROR", 500

#-- News -------------------------------------------------

@api.route('/google-news')
@api.expect(search)
class GetGoogleNews(Resource):
    def post(self, ):    
        try:
            return getGoogleNews(api.payload)
        except:
            print("Error - GetGoogleNews()")
            return "ERROR", 500

