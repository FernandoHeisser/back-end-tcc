from flask_restx import Resource, fields

from src.config.server.instance import server
from src.yfinance.yfinance_repository import *

app, api = server.app, server.api

stockList = api.model('stockList', {
    "stockList": fields.List,
})

@api.route('/yahoo/<string:symbol>')
class GetLastDailyYahooData(Resource):
    def get(self, symbol):
        return getLastDailyYahooData(symbol)

@api.route('/yahoo/<string:symbol>/<string:interval>')
class GetLastYahooData(Resource):
    def get(self, symbol, interval):
        return getLastYahooData(symbol, interval)

@api.route('/yahoo')
class GetLastYahooDataList(Resource):
    def post(self, ):
        return getLastYahooDataList(api.payload)

