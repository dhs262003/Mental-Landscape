from pymongo import MongoClient
from datetime import date

client = MongoClient("mongodb://localhost:27017")
db = client["mind_landscape"]
collection = db["userData"]

def User(name):
    uid = name
    documents = collection.find_one({"Uid": uid})
    
    if "Entries" in documents:
        pass
    else:
        collection.update_one({}, {"$set": {"Entries":[]}})

    pipeline = [
        {"$project": {"count": {"$size": "$Entries"}}}
    ]
    result = list(collection.aggregate(pipeline))
    count = result[0]["count"]

    uName = documents["Uname"]
    print(f"Hey {uName}!\nCheck out your entries below: ")
    
    if count > 0:
        for i in range(count):
            print(str(i+1)+". Date: " + documents["Entries"][i]["Edate"] + "\tYou felt: " + documents["Entries"][i]["Emood"] + "\n\ttype " + str(i+1) + " to view entry\n")

        vChoice = int(input("Enter the number of the entry you want to view: "))
        vChoice-=1
        if vChoice <= count:
            print("Date: " + documents["Entries"][vChoice]["Edate"] + "\nMood: " + documents["Entries"][vChoice]["Emood"] + "\nThoughts: " + documents["Entries"][vChoice]["Ethoughts"])
        else:
            print("Invalid choice.")
    else:
        print("No entries found.")

    choice = str(input("\nWant to make a new entry ? (y/n) :"))
    if choice == "y":
        print("Todays entry:\nDate: " + str(date.today()))
        mood = str(input("Mood: "))
        thoughts = str(input("Thoughts: "))
        newEntry = {"Edate" : str(date.today()), "Emood" : mood, "Ethoughts" : thoughts}
        collection.update_one({}, {"$push": {"Entries": newEntry}})