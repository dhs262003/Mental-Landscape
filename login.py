from pymongo import MongoClient
import hashlib

def Login():

    client = MongoClient("mongodb://localhost:27017")
    db = client["mind_landscape"]
    collection = db["userData"]

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hash_password = hash_object.hexdigest()
    password = hash_password

    user = collection.find_one({"Uid": username, "Upswd": password})
    if user:
        return {"success": True, "username": user["Uid"]}

    return {"success": False, "username": None}