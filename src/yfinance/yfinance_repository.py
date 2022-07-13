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
        print('Error - getCurrentStockDataFromYahoo - ' + symbol)
        return None

def getLastYahooData(symbol, interval):
    try:
        try:
            data = yf.download((str(symbol) + '.SA'), period='1d', interval=interval)
        except:
            data = yf.download(str(symbol), period='1d', interval=interval)

        data = data.reset_index() 
        data = data.iloc[-1]

        try:
            date = str(data['Datetime'])
        except:
            date = str(data['Date'])

        response = {
            'open': str(data['Open']),
            'high': str(data['High']),
            'low': str(data['Low']),
            'close': str(data['Close']),
            'adjClose': str(data['Adj Close']),
            'volume': str(data['Volume']),
            'datetime': date
        }
        
        return response

    except:
        print('Error - getLastYahooData')
        return None

def getLastYahooDataList(request):
    if 'stockList' in request:
        symbols = request['stockList']
    if 'interval' in request and request['interval'] is not None:
        interval = request['interval']
    else:
        interval = '1d'

    stockDatas = []
    for symbol in symbols:

        counter = 0

        while True:
            content = getLastYahooData(symbol, interval)

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

