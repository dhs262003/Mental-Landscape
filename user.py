from pymongo import MongoClient
from datetime import date, datetime

client = MongoClient("mongodb://localhost:27017")
db = client["mind_landscape"]
collection = db["userData"]

def display(name):
    uid = name
    documents = collection.find_one({"Uid": uid})
    
    count = len(documents["Entries"])
    # print(count)

    print("Check out your entries below: ")
    if count > 0:
        for i in range(count):
            print(str(i+1)+". Date-Time: " + documents["Entries"][i]["Edatetime"] + "\tYou felt: " + documents["Entries"][i]["Emood"] + "\n\ttype " + str(i+1) + " to view entry\n")

        vChoice = int(input("Enter the number of the entry you want to view (i -> type 0 to skip): "))
        vChoice-=1
        if 0 <= vChoice <= count:
            print("Date-Time: " + documents["Entries"][vChoice]["Edatetime"] + "\nMood: " + documents["Entries"][vChoice]["Emood"] + "\nThoughts: " + documents["Entries"][vChoice]["Ethoughts"])
        elif vChoice == -1:
            pass
        else:
            print("Invalid choice.")
    else:
        print("No entries found.")

def User(name):
    uid = name
    documents = collection.find_one({"Uid": uid})

    if "Ulocation" in documents:
        collection.update_one( { "Ulocation": { "$size": 3 } }, { "$pop": { "Ulocation" : -1 } } )
    
    if "Entries" in documents:
        pass
    else:
        collection.update_one({"Uid": uid}, {"$set": {"Entries":[]}})
    
    uName = documents["Uname"]
    print(f"Hey {uName}!")

    choice = str(input("\nWant to make a new entry ? (y/n) :"))
    if choice == "y":
        time = str(datetime.now().time().isoformat(timespec='minutes'))
        print("Todays entry:\n\nDate: " + str(date.today()) + "\nTime: " + time)
        moodRate = int(input("How do you feel today? (1-5) (1 = very bad, 5 = very good): "))
        mood = str(input("Mood: "))
        thoughts = str(input("Thoughts: "))
        newEntry = {"Edatetime" : str(date.today()) + f" @ {time}", "EmoodRate" : moodRate,"Emood" : mood, "Ethoughts" : thoughts}
        collection.update_one({"Uid": uid}, {"$push": {"Entries": newEntry}})
        
        display(uid)
    elif choice == "n":
        display(uid)
    else:
        print("Invalid choice.")
    
