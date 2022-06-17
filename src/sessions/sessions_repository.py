

def getSession(id):
    try:
        user = usersDb.find_one({"_id": id})

        if user is None:
            return 404

        userStocks = []

        for stock in user['stocks']:

            try: 
                if not('symbol' in stock and stock['symbol'] is not None):
                    continue

                try:
                    fetchStockData(stock['symbol'])
                except:
                    print('Could not fetch stock data - ' + stock['symbol'])

                stockData = getLastStockData(stock['symbol'])

                stockDataYahoo = getCurrentStockDataFromYahoo(stock['symbol'])

                if not('tags' in stock and stock['tags'] is not None):
                    stock['tags'] = str(stockData['company'] + ', ' + stock['symbol'])

                if not('sources' in stock and stock['sources'] is not None):
                    stock['sources'] = []

                userStocks.append(
                    {
                        'symbol': stock['symbol'],
                        'stockDataYahoo': stockDataYahoo,
                        'stockCurrentData': stockData,
                        'tags': stock['tags'],
                        'sources': stock['sources'],
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
        print('Error UsersRepository - getUserSession()')
        return 500
