from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://fernando:8211@cluster0.efvzz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster["Database-TCC"]

stocksDb = db["Stocks"]
usersDb = db["Users"]
