from pymongo import MongoClient
from datetime import date
import geocoder
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
        loc = geocoder.ip('me')
        saveLoc = str(date.today()) + "; " + loc.city + ", " + loc.state + ", " + loc.country
        collection.update_one({}, {"$push": {"Ulocation" : saveLoc}})
        return {"success": True, "username": user["Uid"]}

    return {"success": False, "username": None}