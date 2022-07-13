from flask_restx import Resource, fields

from src.config.server.instance import server
from src.yfinance.yfinance_repository import *

app, api = server.app, server.api

stockList = api.model('stockList', {
    "stockList": fields.List,
})

@api.route('/yahoo/now/<string:symbol>')
class GetLastDailyYahooData(Resource):
    def get(self, symbol):
        return getLastDailyYahooData(symbol)

@api.route('/yahoo/<string:symbol>')
class GetLastYahooData(Resource):
    def get(self, symbol):
        return getLastYahooData(symbol)

@api.route('/yahoo')
class GetLastYahooDataList(Resource):
    def post(self, ):
        return getLastYahooDataList(api.payload)

