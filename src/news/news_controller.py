from flask_restx import Resource

from src.config.server.instance import server
from src.news.news_webscraper import *

app, api = server.app, server.api

@api.route('/news/<string:tags>')
class GetNews(Resource):
    def get(self, tags):    
        return getNews(tags)