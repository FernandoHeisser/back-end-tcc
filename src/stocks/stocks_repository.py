import uuid
from src.config.database.connection import stocksDb

def getStockBySymbol(symbol):    
    try:
        return list(stocksDb.find({"symbol": str(symbol).upper()}))
    except:
        print('Error - StocksRepository getStockNewsBySymbol()')
        return 500

def getStocks():    
    try:
        stocks = list(stocksDb.find())
        response = {
            'size': len(stocks),
            'content': stocks
        }
        return response
    except:
        print('Error - StocksRepository getStocks()')
        return 500

def createStock(request):
    try:
        stock = {
            "_id": str(uuid.uuid4()),
            "company": request["company"],
            "symbol": request["symbol"],
            "url": request["url"]
        }
        return stocksDb.insert_one(stock).inserted_id
    except:
        print('Error - StocksRepository createStock()')
        return 500

