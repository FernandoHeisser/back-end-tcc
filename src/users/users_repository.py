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

def getUser(id):    
    try:
        user = usersDb.find_one({"_id": id})
        if user is None:
            return "NOT FOUND", 404
        else:
            return user
    except:
        print('Error UsersRepository - getUser()')
        return 500

def deleteUser(id):    
    try:    
        return usersDb.delete_one({"_id": id}).deleted_count
    except:
        print('Error UsersRepository - deleteUser()')
        return 500

