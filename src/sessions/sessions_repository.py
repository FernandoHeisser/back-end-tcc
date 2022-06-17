from src.users.users_repository import getUser
from src.stocks.stocks_repository import getStockBySymbol
from src.yfinance.yfinance_repository import getCurrentStockDataFromYahoo

def getSession(id):
    try:
        user = getUser(id)
        if user is None:
            return None

        userStocks = []
        for stock in user['stocks']:
            try: 
                if 'symbol' in stock and stock['symbol'] is not None:
                    
                    info = getStockBySymbol(stock['symbol'])
                    data = getCurrentStockDataFromYahoo(stock['symbol'])
                    
                    if not('tags' in stock and stock['tags'] is not None):
                        stock['tags'] = str(info['company'] + ', ' + stock['symbol'])

                    userStocks.append(
                        {
                            'symbol': stock['symbol'],
                            'company': info['company'],
                            'data': data,
                            'tags': stock['tags'],
                        }
                    )

            except:
                print('Could not get stock info - ' + stock['symbol'])
                continue

        reponse = {
            'user': user,
            'stocks': userStocks
        }

        return reponse
    except:
        print('Error - getSession')
        return None
