from pymongo import MongoClient
from datetime import date, datetime
import geocoder
from getpass import getpass
import hashlib

def Login():

    client = MongoClient("mongodb://localhost:27017")
    db = client["mind_landscape"]
    collection = db["userData"]

    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hash_password = hash_object.hexdigest()
    password = hash_password

    documents = collection.find_one({"Uid": username})
    countLoc = len(documents["Ulocation"])

    user = collection.find_one({"Uid": username, "Upswd": password})
    if user:
        loc = geocoder.ip('me')
        saveLoc = str(date.today()) + "; " + loc.city + ", " + loc.state + ", " + loc.country + "- @ " + str(datetime.now().time().isoformat(timespec='minutes'))
        if countLoc < 3:
            collection.update_one({"Uid": username}, {"$push": {"Ulocation" : saveLoc}})
        else:
            collection.update_one({"Uid": username}, {"$pop": {"Ulocation" : -1}})
            collection.update_one({"Uid": username}, {"$push": {"Ulocation" : saveLoc}})
        return {"success": True, "username": user["Uid"]}

    return {"success": False, "username": None}