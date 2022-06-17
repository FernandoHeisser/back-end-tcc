from flask_restx import Resource, fields

from src.config.server.instance import server
from yfinance.yfinance_repository import *

app, api = server.app, server.api

stockList = api.model('stockList', {
    "stockList": fields.List,
})

@api.route('/yahoo/now/<string:symbol>')
class GetCurrentStockDataFromYahoo(Resource):
    def get(self, symbol):
        return getCurrentStockDataFromYahoo(symbol)

@api.route('/yahoo/<string:symbol>')
class GetFirstOfTheDayAndCurrentStockDataFromYahoo(Resource):
    def get(self, symbol):
        return getFirstOfTheDayAndCurrentStockDataFromYahoo(symbol)

@api.route('/yahoo/now')
class GetCurrentStockDataFromYahooList(Resource):
    def post(self, ):
        return getCurrentStockDataFromYahooList(api.payload)

@api.route('/yahoo')
class GetFirstOfTheDayAndCurrentStockDataFromYahooList(Resource):
    def post(self, ):
        return getFirstOfTheDayAndCurrentStockDataFromYahooList(api.payload)

