import uuid
from src.config.database.connection import stocksDb

def getStockBySymbol(symbol):    
    try:
        return stocksDb.find_one({"symbol": str(symbol).upper()})

    except:
        print('Error - getStockNewsBySymbol')
        return None

def getStocks():    
    try:
        stocks = list(stocksDb.find())
        response = {
            'size': len(stocks),
            'content': stocks
        }
        return response

    except:
        print('Error - getStocks')
        return None

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
        print('Error - createStock')
        return None

