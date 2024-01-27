from pymongo import MongoClient
from datetime import date, datetime
import hashlib
import geocoder
from getpass import getpass
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def check(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def Signup():

    client = MongoClient("mongodb://localhost:27017")
    db = client["mind_landscape"]
    collection = db["userData"]

    username = str(input("Choose a username: "))
    if len(username) < 4:
        print("Username should be at least 4 characters long.")
        return

    existing_user = collection.find_one({"Uid" : username})

    # print(existing_user)

    if existing_user:
        print("Username already exists, please choose a different username.")
        return   
    else:
        password = getpass("Choose a password: ")
        if len(password) < 8:
            print("Password should be at least 8 characters long.")
            return
        else:
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            age = int(input("Enter your age: "))
            calcuDOY = datetime.now().year - age
            loc = input("Enter your location(city, state, country): ")
            loc = geocoder.ip('me')
            saveLoc = str(date.today()) + "; " + loc.city + ", " + loc.state + ", " + loc.country + "- @ " + str(datetime.now().time().isoformat(timespec='minutes'))
            if check(email):
                hash_object = hashlib.sha256()
                hash_object.update(password.encode())
                hash_password = hash_object.hexdigest()
                password = hash_password

                user_data = {"Uid": username, "Upswd": password, "Uname": name, "Uemail": email, "Uage": age, "Udoy": calcuDOY ,"Ulocation": [saveLoc]}
                collection.insert_one(user_data)
                print("Sign up successful!\n\nLogin to continue.\n")

            else:
                print("Invalid email address.\nSign up failed. Please try again.")
