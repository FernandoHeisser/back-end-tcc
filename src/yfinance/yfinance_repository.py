import yfinance as yf

def getCurrentStockDataFromYahoo(symbol):
    try:
        today_data = yf.download(tickers=(str(symbol) + '.SA'), period='1d', interval='1m')
        today_data = today_data.reset_index() 

        today_initial_row = today_data.iloc[0]
        today_final_row = today_data.iloc[-1]

        return {
            'open': str(today_initial_row['Open']),
            'high': str(today_final_row['High']),
            'low': str(today_final_row['Low']),
            'close': str(today_final_row['Close']),
            'adjClose': str(today_final_row['Adj Close']),
            'volume': str(today_final_row['Volume']),
            'datetime': str(today_final_row['Datetime'])
        }
        
    except:
        return "ERROR", 500

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

