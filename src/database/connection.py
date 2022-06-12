from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://fernando:8211@cluster0.efvzz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster["Database-TCC"]

stockNewsDb = db["StockNews"]
stocksDb = db["Stocks"]
stockDataDb = db["StockData"]
usersDb = db["Users"]
sourcesDb = db["Sources"]
googleNewsDb = db["GoogleNews"]
