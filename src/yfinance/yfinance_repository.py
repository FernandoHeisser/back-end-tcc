import yfinance as yf

def getLastDailyYahooData(symbol):
    try:
        try:
            today_data = yf.download((str(symbol) + '.SA'), period='1d', interval='1d')
        except:
            today_data = yf.download(str(symbol), period='1d', interval='1d')

        today_data = today_data.reset_index()

        try:
            now_data = yf.download((str(symbol) + '.SA'), period='1d', interval='1m')
        except:
            now_data = yf.download(str(symbol), period='1d', interval='1m')
        
        now_data = now_data.reset_index() 

        today_data = today_data.iloc[0]
        now_data = now_data.iloc[-1]

        try:
            _datetime = str(now_data['Datetime'])
        except:
            _datetime = str(now_data['Date'])

        return {
            'high': str(today_data['High']),
            'low': str(today_data['Low']),
            'current': str(now_data['Close']),
            'datetime': _datetime
        }    
    except:
        print('Error - getLastDailyYahooData - ' + symbol)
        return None

def getLastYahooData(symbol):
    try:
        try:
            yesterday_data = yf.download((str(symbol) + '.SA'), period='2d', interval='1d')
        except:
            yesterday_data = yf.download(str(symbol), period='2d', interval='1d')

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

        try:
            today_data = yf.download((str(symbol) + '.SA'), period='1d', interval='1h')
        except:
            today_data = yf.download(str(symbol), period='1d', interval='1h')

        today_data = today_data.reset_index()
        today_data = today_data.iloc[0]

        try:
            day = yf.download((str(symbol) + '.SA'), period='1d', interval='1d')
        except:
            day = yf.download(str(symbol), period='1d', interval='1d')

        day = day.reset_index()
        day = day.iloc[0]

        try:
            today_last_data = yf.download((str(symbol) + '.SA'), period='1d', interval='1m')
        except:
            today_last_data = yf.download(str(symbol), period='1d', interval='1m')

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
        print('Error - getLastYahooData - ' + symbol)
        return None

def getLastYahooDataList(stockList):
    symbols = stockList['stockList']

    stockDatas = []


    for symbol in symbols:

        counter = 0

        while True:
            content = getLastYahooData(symbol)

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

