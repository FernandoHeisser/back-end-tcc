import yfinance as yf

def getCurrentStockDataFromYahoo(symbol):
    try:
        today_data = yf.download(tickers=(str(symbol) + '.SA'), period='1d', interval='1d')
        today_data = today_data.reset_index()

        now_data = yf.download(tickers=(str(symbol) + '.SA'), period='1d', interval='1m')
        now_data = now_data.reset_index() 

        today_data = today_data.iloc[0]
        now_data = now_data.iloc[-1]

        return {
            'high': str(today_data['High']),
            'low': str(today_data['Low']),
            'current': str(now_data['Close']),
            'datetime': str(now_data['Datetime'])
        }    
    except:
        print('Error - getCurrentStockDataFromYahoo')
        return None

def getFirstOfTheDayAndCurrentStockDataFromYahoo(symbol):
    try:
        yesterday_data = yf.download(tickers=(str(symbol) + '.SA'), period='2d', interval='1d')
        yesterday_data = yesterday_data.reset_index() 
        yesterday_data = yesterday_data.iloc[0]

        yesterday = {
            'open': str(yesterday_data['Open']),
            'high': str(yesterday_data['High']),
            'low': str(yesterday_data['Low']),
            'close': str(yesterday_data['Close']),
            'adjClose': str(yesterday_data['Adj Close']),
            'volume': str(yesterday_data['Volume']),
            'datetime': str(yesterday_data['Date'])
        }

        today_data = yf.download(tickers=(str(symbol) + '.SA'), period='1d', interval='1h')
        today_data = today_data.reset_index()
        today_data = today_data.iloc[0]

        day = yf.download(tickers=(str(symbol) + '.SA'), period='1d', interval='1d')
        day = day.reset_index()
        day = day.iloc[0]

        today_last_data = yf.download(tickers=(str(symbol) + '.SA'), period='1d', interval='1m')
        today_last_data = today_last_data.reset_index() 
        today_last_data = today_last_data.iloc[-1]

        today = {
            'open': str(day['Open']),
            'high': str(day['High']),
            'low': str(day['Low']),
            'close': str(today_last_data['Close']),
            'adjClose': str(today_last_data['Adj Close']),
            'volume': str(day['Volume']),
            'datetime': str(today_last_data['Datetime'])
        }
        
        return {
            'yesterday': yesterday,
            'today': today
        }

    except:
        print('Error - getFirstOfTheDayAndCurrentStockDataFromYahoo')
        return None

def getCurrentStockDataFromYahooList(stockList):
    symbols = stockList['stockList']

    stockDatas = []

    for symbol in symbols:

        counter = 0

        while True:
            content = getCurrentStockDataFromYahoo(symbol)

            counter = counter + 1

            if content is not None:
                break
            if counter >= 10: 
                break

        stockDatas.append({
            'symbol': symbol,
            'content': content
        })

    return stockDatas

def getFirstOfTheDayAndCurrentStockDataFromYahooList(stockList):
    symbols = stockList['stockList']

    stockDatas = []


    for symbol in symbols:

        counter = 0

        while True:
            content = getFirstOfTheDayAndCurrentStockDataFromYahoo(symbol)

            counter = counter + 1

            if content is not None:
                break
            if counter >= 10: 
                break

        stockDatas.append({
            'symbol': symbol,
            'content': content
        })

    return stockDatas

