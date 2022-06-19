from src.users.users_repository import getUser
from src.stocks.stocks_repository import getStockBySymbol
from src.yfinance.yfinance_repository import getCurrentStockDataFromYahoo
from src.news.news_webscraper import getNews

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
                    
                    if 'tags' not in stock or stock['tags'] is None or stock['tags'] == '':
                        stock['tags'] = str(info['company'] + '+' + stock['symbol']).replace(' ', '+')

                    news = getNews(stock['tags'])

                    userStocks.append(
                        {
                            'symbol': stock['symbol'],
                            'company': info['company'],
                            'tags': stock['tags'],
                            'data': data,
                            'news': news
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
