import yfinance as yf

def getLastYahooData(symbol):
    try:
        data = yf.download((str(symbol) + '.SA'), period='1d', interval='1d')

        data = data.reset_index()
        data = data.iloc[-1]

        return {
            'high': str(data['High']),
            'low': str(data['Low']),
            'current': str(data['Close']),
            'datetime': str(data['Date'])
        }    
    except:
        print('Error - getLastYahooData - ' + symbol)
        return None

def getLastYahooDataOneMinute(symbol):
    try:
        data = yf.download((str(symbol) + '.SA'), period='60m', interval='1m')
        data = data.reset_index() 

        previous_minute_data = data.iloc[-2]
        current_minute_data = data.iloc[-1]

        yesterday = {
            'open': str(previous_minute_data['Open']),
            'high': str(previous_minute_data['High']),
            'low': str(previous_minute_data['Low']),
            'close': str(previous_minute_data['Close']),
            'adjClose': str(previous_minute_data['Adj Close']),
            'volume': str(previous_minute_data['Volume']),
            'datetime': str(previous_minute_data['Datetime'])
        }

        today = {
            'open': str(current_minute_data['Open']),
            'high': str(current_minute_data['High']),
            'low': str(current_minute_data['Low']),
            'close': str(current_minute_data['Close']),
            'adjClose': str(current_minute_data['Adj Close']),
            'volume': str(current_minute_data['Volume']),
            'datetime': str(current_minute_data['Datetime'])
        }
        
        return {
            'yesterday': yesterday,
            'today': today
        }

    except:
        print('Error - getLastYahooDataOneMinute - ' + symbol)
        return None

def getLastYahooDataTwoMinutes(symbol):
    try:
        data = yf.download((str(symbol) + '.SA'), period='60m', interval='2m')
        data = data.reset_index() 

        previous_minute_data = data.iloc[-2]
        current_minute_data = data.iloc[-1]

        yesterday = {
            'open': str(previous_minute_data['Open']),
            'high': str(previous_minute_data['High']),
            'low': str(previous_minute_data['Low']),
            'close': str(previous_minute_data['Close']),
            'adjClose': str(previous_minute_data['Adj Close']),
            'volume': str(previous_minute_data['Volume']),
            'datetime': str(previous_minute_data['Datetime'])
        }

        today = {
            'open': str(current_minute_data['Open']),
            'high': str(current_minute_data['High']),
            'low': str(current_minute_data['Low']),
            'close': str(current_minute_data['Close']),
            'adjClose': str(current_minute_data['Adj Close']),
            'volume': str(current_minute_data['Volume']),
            'datetime': str(current_minute_data['Datetime'])
        }
        
        return {
            'yesterday': yesterday,
            'today': today
        }

    except:
        print('Error - getLastYahooDataTwoMinutes - ' + symbol)
        return None

def getLastYahooDataFiveMinutes(symbol):
    try:
        data = yf.download((str(symbol) + '.SA'), period='60m', interval='5m')
        data = data.reset_index() 

        previous_minute_data = data.iloc[-2]
        current_minute_data = data.iloc[-1]

        yesterday = {
            'open': str(previous_minute_data['Open']),
            'high': str(previous_minute_data['High']),
            'low': str(previous_minute_data['Low']),
            'close': str(previous_minute_data['Close']),
            'adjClose': str(previous_minute_data['Adj Close']),
            'volume': str(previous_minute_data['Volume']),
            'datetime': str(previous_minute_data['Datetime'])
        }

        today = {
            'open': str(current_minute_data['Open']),
            'high': str(current_minute_data['High']),
            'low': str(current_minute_data['Low']),
            'close': str(current_minute_data['Close']),
            'adjClose': str(current_minute_data['Adj Close']),
            'volume': str(current_minute_data['Volume']),
            'datetime': str(current_minute_data['Datetime'])
        }
        
        return {
            'yesterday': yesterday,
            'today': today
        }

    except:
        print('Error - getLastYahooDataFiveMinutes - ' + symbol)
        return None

def getLastYahooDataFifteenMinutes(symbol):
    try:
        data = yf.download((str(symbol) + '.SA'), period='60m', interval='15m')
        data = data.reset_index() 

        previous_minute_data = data.iloc[-2]
        current_minute_data = data.iloc[-1]

        yesterday = {
            'open': str(previous_minute_data['Open']),
            'high': str(previous_minute_data['High']),
            'low': str(previous_minute_data['Low']),
            'close': str(previous_minute_data['Close']),
            'adjClose': str(previous_minute_data['Adj Close']),
            'volume': str(previous_minute_data['Volume']),
            'datetime': str(previous_minute_data['Datetime'])
        }

        today = {
            'open': str(current_minute_data['Open']),
            'high': str(current_minute_data['High']),
            'low': str(current_minute_data['Low']),
            'close': str(current_minute_data['Close']),
            'adjClose': str(current_minute_data['Adj Close']),
            'volume': str(current_minute_data['Volume']),
            'datetime': str(current_minute_data['Datetime'])
        }
        
        return {
            'yesterday': yesterday,
            'today': today
        }

    except:
        print('Error - getLastYahooDataFifteenMinutes - ' + symbol)
        return None

def getLastYahooDataThirtyMinutes(symbol):
    try:
        data = yf.download((str(symbol) + '.SA'), period='60m', interval='30m')
        data = data.reset_index() 

        previous_minute_data = data.iloc[-2]
        current_minute_data = data.iloc[-1]

        yesterday = {
            'open': str(previous_minute_data['Open']),
            'high': str(previous_minute_data['High']),
            'low': str(previous_minute_data['Low']),
            'close': str(previous_minute_data['Close']),
            'adjClose': str(previous_minute_data['Adj Close']),
            'volume': str(previous_minute_data['Volume']),
            'datetime': str(previous_minute_data['Datetime'])
        }

        today = {
            'open': str(current_minute_data['Open']),
            'high': str(current_minute_data['High']),
            'low': str(current_minute_data['Low']),
            'close': str(current_minute_data['Close']),
            'adjClose': str(current_minute_data['Adj Close']),
            'volume': str(current_minute_data['Volume']),
            'datetime': str(current_minute_data['Datetime'])
        }
        
        return {
            'yesterday': yesterday,
            'today': today
        }

    except:
        print('Error - getLastYahooDataThirtyMinutes - ' + symbol)
        return None

def getLastYahooDataNinetyMinutes(symbol):
    try:
        data = yf.download((str(symbol) + '.SA'), period='120m', interval='90m')
        data = data.reset_index() 

        previous_minute_data = data.iloc[-2]
        current_minute_data = data.iloc[-1]

        yesterday = {
            'open': str(previous_minute_data['Open']),
            'high': str(previous_minute_data['High']),
            'low': str(previous_minute_data['Low']),
            'close': str(previous_minute_data['Close']),
            'adjClose': str(previous_minute_data['Adj Close']),
            'volume': str(previous_minute_data['Volume']),
            'datetime': str(previous_minute_data['Datetime'])
        }

        today = {
            'open': str(current_minute_data['Open']),
            'high': str(current_minute_data['High']),
            'low': str(current_minute_data['Low']),
            'close': str(current_minute_data['Close']),
            'adjClose': str(current_minute_data['Adj Close']),
            'volume': str(current_minute_data['Volume']),
            'datetime': str(current_minute_data['Datetime'])
        }
        
        return {
            'yesterday': yesterday,
            'today': today
        }

    except:
        print('Error - getLastYahooDataNinetyMinutes - ' + symbol)
        return None

def getLastYahooDataOneHour(symbol):
    try:
        data = yf.download((str(symbol) + '.SA'), period='2h', interval='1h')
        data = data.reset_index() 

        previous_hour_data = data.iloc[-2]
        current_hour_data = data.iloc[-1]

        yesterday = {
            'open': str(previous_hour_data['Open']),
            'high': str(previous_hour_data['High']),
            'low': str(previous_hour_data['Low']),
            'close': str(previous_hour_data['Close']),
            'adjClose': str(previous_hour_data['Adj Close']),
            'volume': str(previous_hour_data['Volume']),
            'datetime': str(previous_hour_data['index'])
        }

        today = {
            'open': str(current_hour_data['Open']),
            'high': str(current_hour_data['High']),
            'low': str(current_hour_data['Low']),
            'close': str(current_hour_data['Close']),
            'adjClose': str(current_hour_data['Adj Close']),
            'volume': str(current_hour_data['Volume']),
            'datetime': str(current_hour_data['index'])
        }
        
        return {
            'yesterday': yesterday,
            'today': today
        }

    except:
        print('Error - getLastYahooDataOneHour - ' + symbol)
        return None

def getLastYahooDataOneDay(symbol):
    try:
        data = yf.download((str(symbol) + '.SA'), period='2d', interval='1d')
        data = data.reset_index() 

        yesterday_data = data.iloc[-2]
        today_data = data.iloc[-1]

        yesterday = {
            'open': str(yesterday_data['Open']),
            'high': str(yesterday_data['High']),
            'low': str(yesterday_data['Low']),
            'close': str(yesterday_data['Close']),
            'adjClose': str(yesterday_data['Adj Close']),
            'volume': str(yesterday_data['Volume']),
            'datetime': str(yesterday_data['Date'])
        }

        today = {
            'open': str(today_data['Open']),
            'high': str(today_data['High']),
            'low': str(today_data['Low']),
            'close': str(today_data['Close']),
            'adjClose': str(today_data['Adj Close']),
            'volume': str(today_data['Volume']),
            'datetime': str(today_data['Date'])
        }
        
        return {
            'yesterday': yesterday,
            'today': today
        }

    except:
        print('Error - getLastYahooDataOneDay - ' + symbol)
        return None

def getLastYahooDataFiveDays(symbol):
    try:
        data = yf.download((str(symbol) + '.SA'), period='10d', interval='5d')
        data = data.reset_index() 

        previous_days_data = data.iloc[-2]
        current_days_data = data.iloc[-1]

        yesterday = {
            'open': str(previous_days_data['Open']),
            'high': str(previous_days_data['High']),
            'low': str(previous_days_data['Low']),
            'close': str(previous_days_data['Close']),
            'adjClose': str(previous_days_data['Adj Close']),
            'volume': str(previous_days_data['Volume']),
            'datetime': str(previous_days_data['Date'])
        }

        today = {
            'open': str(current_days_data['Open']),
            'high': str(current_days_data['High']),
            'low': str(current_days_data['Low']),
            'close': str(current_days_data['Close']),
            'adjClose': str(current_days_data['Adj Close']),
            'volume': str(current_days_data['Volume']),
            'datetime': str(current_days_data['Date'])
        }
        
        return {
            'yesterday': yesterday,
            'today': today
        }

    except:
        print('Error - getLastYahooDataFiveDays - ' + symbol)
        return None

def getLastYahooDataOneWeek(symbol):
    try:
        data = yf.download((str(symbol) + '.SA'), period='2wk', interval='1wk')
        data = data.reset_index() 

        previous_week_data = data.iloc[-2]
        current_week_data = data.iloc[-1]

        yesterday = {
            'open': str(previous_week_data['Open']),
            'high': str(previous_week_data['High']),
            'low': str(previous_week_data['Low']),
            'close': str(previous_week_data['Close']),
            'adjClose': str(previous_week_data['Adj Close']),
            'volume': str(previous_week_data['Volume']),
            'datetime': str(previous_week_data['Date'])
        }

        today = {
            'open': str(current_week_data['Open']),
            'high': str(current_week_data['High']),
            'low': str(current_week_data['Low']),
            'close': str(current_week_data['Close']),
            'adjClose': str(current_week_data['Adj Close']),
            'volume': str(current_week_data['Volume']),
            'datetime': str(current_week_data['Date'])
        }
        
        return {
            'yesterday': yesterday,
            'today': today
        }

    except:
        print('Error - getLastYahooDataOneWeek - ' + symbol)
        return None

def getLastYahooDataOneMonth(symbol):
    try:
        data = yf.download((str(symbol) + '.SA'), period='2mo', interval='1mo')
        data = data.reset_index() 

        previous_month_data = data.iloc[-2]
        current_month_data = data.iloc[-1]

        yesterday = {
            'open': str(previous_month_data['Open']),
            'high': str(previous_month_data['High']),
            'low': str(previous_month_data['Low']),
            'close': str(previous_month_data['Close']),
            'adjClose': str(previous_month_data['Adj Close']),
            'volume': str(previous_month_data['Volume']),
            'datetime': str(previous_month_data['Date'])
        }

        today = {
            'open': str(current_month_data['Open']),
            'high': str(current_month_data['High']),
            'low': str(current_month_data['Low']),
            'close': str(current_month_data['Close']),
            'adjClose': str(current_month_data['Adj Close']),
            'volume': str(current_month_data['Volume']),
            'datetime': str(current_month_data['Date'])
        }
        
        return {
            'yesterday': yesterday,
            'today': today
        }

    except:
        print('Error - getLastYahooDataOneMonth - ' + symbol)
        return None

def getLastYahooDataThreeMonths(symbol):
    try:
        data = yf.download((str(symbol) + '.SA'), period='6mo', interval='3mo')
        data = data.reset_index() 

        previous_months_data = data.iloc[-2]
        current_months_data = data.iloc[-1]

        yesterday = {
            'open': str(previous_months_data['Open']),
            'high': str(previous_months_data['High']),
            'low': str(previous_months_data['Low']),
            'close': str(previous_months_data['Close']),
            'adjClose': str(previous_months_data['Adj Close']),
            'volume': str(previous_months_data['Volume']),
            'datetime': str(previous_months_data['Date'])
        }

        today = {
            'open': str(current_months_data['Open']),
            'high': str(current_months_data['High']),
            'low': str(current_months_data['Low']),
            'close': str(current_months_data['Close']),
            'adjClose': str(current_months_data['Adj Close']),
            'volume': str(current_months_data['Volume']),
            'datetime': str(current_months_data['Date'])
        }
        
        return {
            'yesterday': yesterday,
            'today': today
        }

    except:
        print('Error - getLastYahooDataThreeMonths - ' + symbol)
        return None

def getData(symbol, interval):
    if interval == '1m':
        return getLastYahooDataOneMinute(symbol)
    if interval == '2m':
        return getLastYahooDataTwoMinutes(symbol)
    if interval == '5m':
        return getLastYahooDataFiveMinutes(symbol)
    if interval == '15m':
        return getLastYahooDataFifteenMinutes(symbol)
    if interval == '30m':
        return getLastYahooDataThirtyMinutes(symbol)
    if interval == '60m':
        return getLastYahooDataOneHour(symbol)
    if interval == '90m':
        return getLastYahooDataNinetyMinutes(symbol)
    if interval == '1h':
        return getLastYahooDataOneHour(symbol)
    if interval == '1d':
        return getLastYahooDataOneDay(symbol)
    if interval == '5d':
        return getLastYahooDataFiveDays(symbol)
    if interval == '1wk':
        return getLastYahooDataOneWeek(symbol)
    if interval == '1mo':
        return getLastYahooDataOneMonth(symbol)
    if interval == '3mo':
        return getLastYahooDataThreeMonths(symbol)

def getLastYahooDataList(input):
    symbols = input['stockList']
    interval = input['interval']

    stockDatas = []

    for symbol in symbols:
        content = getData(symbol, interval)

        stockDatas.append({
            'symbol': symbol,
            'content': content
        })

    return stockDatas

