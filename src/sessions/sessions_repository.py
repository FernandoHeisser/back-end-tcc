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
                symbol = stock['symbol']

                info = getStockBySymbol(symbol)
                data = getCurrentStockDataFromYahoo(symbol)
                
                tags = str(info['company'] + '+' + info['symbol']).replace(' ', '+')

                news = getNews(tags)

                userStocks.append(
                    {
                        'symbol': info['symbol'],
                        'company': info['company'],
                        'tags': tags,
                        'data': data,
                        'news': news
                    }
                )
            except:
                print('Could not get stock session - ' + symbol)
                continue

        reponse = {
            'user': user,
            'stocks': userStocks
        }

        return reponse
    except:
        print('Error - getSession')
        return None
