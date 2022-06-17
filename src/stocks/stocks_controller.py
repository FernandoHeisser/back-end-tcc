from flask_restx import Resource, fields

from src.config.server.instance import server
from stocks.stocks_webscraper import *
from stocks.stocks_repository import *

app, api = server.app, server.api

stock = api.model('stock', {
    "company": fields.String,
    "symbol": fields.String,
    "url": fields.String
})

@api.route('/stocks/<string:symbol>')
class GetStockBySymbol(Resource):
    def get(self, symbol):    
        return getStockBySymbol(symbol)

@api.route('/stocks')
class GetStocks(Resource):
    def get(self, ):    
        return getStocks()

@api.route('/stocks/fetch')
class FetchStocks(Resource):
    def get(self, ):    
        return fetchStocks()

@api.route('/stocks/add')
class AddStocks(Resource):
    def post(self, ):
        return createStock(api.payload)

