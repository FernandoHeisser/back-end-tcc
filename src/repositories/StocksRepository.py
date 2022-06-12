import uuid
import pymongo
import yfinance as yf
from datetime import date
from src.database.connection import stockNewsDb, stocksDb, stockDataDb

def getStockNews(symbol):
    try:
        stockNews = list(stockNewsDb.find({"symbol": str(symbol).upper()}).sort("date", pymongo.DESCENDING))
        response = {
            'size': len(stockNews),
            'content': stockNews
        }
        return response
    except:
        print('Error - StocksRepository getStockNews()')
        return 500  

def getLastStockData(symbol):
    try:
        stockDatalist = list(stockDataDb.find({"symbol": str(symbol).upper()}).sort("date", pymongo.DESCENDING))
        if len(stockDatalist) > 0:
            return stockDatalist[0]
        return None
    except:
        print('Error - StocksRepository getLastStockData()')
        return 500

def getAllStockData(symbol):
    try:
        stockDatalist = list(stockDataDb.find({"symbol": str(symbol).upper()}).sort("date", pymongo.DESCENDING))
        response = {
            'size': len(stockDatalist),
            'content': stockDatalist
        }
        return response
    except:
        print('Error - StocksRepository getAllStockData()')
        return 500

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

def getCurrentStockDataFromYahoo(symbol):
    try:
        data = yf.download(tickers=(str(symbol) + '.SA'), period='1d', interval='1d')
        data = data.reset_index() 

        final_row = data.iloc[0]

        return {
            'open': str(final_row['Open']),
            'high': str(final_row['High']),
            'low': str(final_row['Low']),
            'close': str(final_row['Close']),
            'adjClose': str(final_row['Adj Close']),
            'volume': str(final_row['Volume']),
            'date': str(final_row['Date'])
        }
    except:
        return 'ERROR', 500

def getFirstOfTheDayAndCurrentStockDataFromYahoo(symbol):
    try:
        yesterday_data = yf.download(tickers=(str(symbol) + '.SA'), period='2d', interval='1m')
        yesterday_data = yesterday_data.reset_index() 

        yesterday_initial_row = yesterday_data.iloc[0]

        yesterday = {
            'open': str(yesterday_initial_row['Open']),
            'high': str(yesterday_initial_row['High']),
            'low': str(yesterday_initial_row['Low']),
            'close': str(yesterday_initial_row['Close']),
            'adjClose': str(yesterday_initial_row['Adj Close']),
            'volume': str(yesterday_initial_row['Volume']),
            'datetime': str(yesterday_initial_row['Datetime'])
        }

        today_data = yf.download(tickers=(str(symbol) + '.SA'), period='1d', interval='1m')
        today_data = today_data.reset_index() 

        today_initial_row = today_data.iloc[0]
        today_final_row = today_data.iloc[-1]

        today = {
            'open': str(today_initial_row['Open']),
            'high': str(today_final_row['High']),
            'low': str(today_final_row['Low']),
            'close': str(today_final_row['Close']),
            'adjClose': str(today_final_row['Adj Close']),
            'volume': str(today_final_row['Volume']),
            'datetime': str(today_final_row['Datetime'])
        }
        
        return {
            'yesterday': yesterday,
            'today': today
        }

    except:
        return 'ERROR', 500

def getCurrentStockDataFromYahooList(stockList):
    symbols = stockList['stockList']

    stockDatas = []

    for symbol in symbols:
        stockDatas.append({
            'symbol': symbol,
            'content': getCurrentStockDataFromYahoo(symbol)
        })

    return stockDatas

def getFirstOfTheDayAndCurrentStockDataFromYahooList(stockList):
    symbols = stockList['stockList']

    stockDatas = []

    for symbol in symbols:
        stockDatas.append({
            'symbol': symbol,
            'content': getFirstOfTheDayAndCurrentStockDataFromYahoo(symbol)
        })

    return stockDatas

