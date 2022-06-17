import uuid

from src.config.database.connection import usersDb

def getUsers():
    try:
        users = list(usersDb.find())
        response = {
            'size': len(users),
            'content': users
        }
        return response
    except:
        print('Error - getUsers')
        return None

def createUser(request):
    try:
        user = {
            "_id": str(uuid.uuid4()),
            "stocks": request['stocks']
        }

        return usersDb.insert_one(user).inserted_id
    except:
        print('Error - createUser')
        return None

def updateUser(user):
    try:
        if "_id" in user and user["_id"] is not None:
            condition = {"_id": user["_id"]}
            data = {"$set": {"stocks": user["stocks"]}}

            usersDb.update_one(condition, data)
    
            return user
        else:
            return None
    except:
        print('Error - updateUser')
        return None

def getUser(id):    
    try:
        return usersDb.find_one({"_id": id})
    except:
        print('Error - getUser')
        return None

def deleteUser(id):    
    try:    
        return usersDb.delete_one({"_id": id}).deleted_count
    except:
        print('Error - deleteUser')
        return None

