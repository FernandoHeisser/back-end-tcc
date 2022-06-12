import uuid

from src.database.connection import usersDb
from src.repositories.StocksRepository import *
from src.google.news import *
from src.webscraping.scraper import *

def getUsers():
    try:
        users = list(usersDb.find())
        response = {
            'size': len(users),
            'content': users
        }
        return response
    except:
        print('Error UsersRepository - getUsers()')
        return 500

def createUser(request):
    try:
        user = {
            "_id": str(uuid.uuid4()),
            "stocks": request['stocks']
        }

        return usersDb.insert_one(user).inserted_id
    except:
        print('Error UsersRepository - createUser()')
        return 500

def updateUser(user):
    try:
        if "_id" in user and user["_id"] is not None:
            condition = {"_id": user["_id"]}
            data = {"$set": {"stocks": user["stocks"]}}

            usersDb.update_one(condition, data)
    
            return user
        else:
            return 400
    except:
        print('Error UsersRepository - updateUser()')
        return 500

def deleteUsers():    
    try:
        return usersDb.delete_many({}).deleted_count
    except:
        print('Error UsersRepository - deleteUsers()')
        return 500

def getUser(id):    
    try:
        return usersDb.find_one({"_id": id})
    except:
        print('Error UsersRepository - getUser()')
        return 500

def deleteUser(id):    
    try:    
        return usersDb.delete_one({"_id": id}).deleted_count
    except:
        print('Error UsersRepository - deleteUser()')
        return 500

def getUserSession(id):
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
                        'stockDataYahoo': stockDataYahoo,
                        'stockCurrentData': stockData,
                        'stockNews': getStockNews(stock['symbol']),
                        'tags': stock['tags'],
                        'sources': stock['sources'],
                        'googleNews': getGoogleNews({
                            'keywords': stock['tags'],
                            'sources': stock['sources']
                        })
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

def fetchUserSession(id):
    try:
        user = usersDb.find_one({"_id": id})

        for stock in user['stocks']:
            if 'symbol' in stock and stock['symbol'] is not None:
                fetchStockNews(stock['symbol'])
            
        return 200
    except:
        print('Error UsersRepository - fetchUserSession()')
        return 500

