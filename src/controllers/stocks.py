from flask_restx import Resource, fields

from src.server.instance import server
from src.webscraping.scraper import *
from src.repositories.StocksRepository import *

app, api = server.app, server.api

stock = api.model('stock', {
    "company": fields.String,
    "symbol": fields.String,
    "url": fields.String
})

stockList = api.model('stockList', {
    "stockList": fields.List,
})

#-- StockNews -----------------------------------------------

@api.route('/stocks/news/all/<string:symbol>')
class GetStockNewsByStockSymbol(Resource):
    def get(self, symbol):
        return getStockNews(symbol)

@api.route('/stocks/news/fetch/<string:symbol>')
class FetchStockNewsByStockSymbol(Resource):
    def get(self, symbol):
        try:
            return fetchStockNews(symbol)
        except:
            print('Error - fetchStockNews()')
            return "ERROR", 500   

#-- StockData -----------------------------------------------
@api.route('/stocks/data/<string:symbol>')
class GetLastStockDataByStockSymbol(Resource):
    def get(self, symbol):
        return getLastStockData(symbol)

@api.route('/stocks/data/all/<string:symbol>')
class GetAllStockDataByStockSymbol(Resource):
    def get(self, symbol):
        return getAllStockData(symbol)

@api.route('/stocks/data/fetch/<string:symbol>')
class FetchStocksDataByStockSymbol(Resource):
    def get(self, symbol):
        try:
            return fetchStockData(symbol)
        except:
            print('Error - fetchStockData()')
            return "ERROR", 500

#-- StockData Yahoo -----------------------------------------
@api.route('/stock/data/yahoo/now/<string:symbol>')
class GetCurrentStockDataFromYahoo(Resource):
    def get(self, symbol):
        return getCurrentStockDataFromYahoo(symbol)

@api.route('/stock/data/yahoo/<string:symbol>')
class GetFirstOfTheDayAndCurrentStockDataFromYahoo(Resource):
    def get(self, symbol):
        return getFirstOfTheDayAndCurrentStockDataFromYahoo(symbol)

@api.route('/stock/data/yahoo/now/list')
class GetCurrentStockDataFromYahooList(Resource):
    def post(self, ):
        return getCurrentStockDataFromYahooList(api.payload)

@api.route('/stock/data/yahoo/list')
class GetFirstOfTheDayAndCurrentStockDataFromYahooList(Resource):
    def post(self, ):
        return getFirstOfTheDayAndCurrentStockDataFromYahooList(api.payload)

#-- Stocks --------------------------------------------------

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

