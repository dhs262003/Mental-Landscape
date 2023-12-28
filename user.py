from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["mind_landscape"]
collection = db["userData"]

def User(name):
    uname = name
    documents = collection.find_one({"Uid": uname})
    print("User class " + documents["Uname"])
    # documents = collection.find_one({"Uid": uname})
    # print(documents)