from pymongo import MongoClient
from moodStats import stats
from datetime import date, datetime
from activityTracker import tracker

client = MongoClient("mongodb://localhost:27017")
db = client["mind_landscape"]
collection = db["userData"]

def forward(name, result):
    while result:
        uid = name
        print("Type 1 to view your stats\nType 2 to view your Activity Tracker\nType 3 to start a breathing session\nType 4 to exit the program")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            print("\nHeres your mood rating statistics: ")
            stats(uid)
            forward(uid, result)
        elif choice == 2:
            print("\nHeres your Activity Tracker: ")
            tracker(uid, result)
        elif choice == 3:
            print("\nHeres your breathing session: ")
            forward(uid, result)
        elif choice == 4:
            print("Thank you for using Mental Landscape.\nExiting...")
            exit()
        else:
            print("Invalid choice. Please enter a valid choice.")
            forward(uid, result)

def display(name):
    uid = name
    documents = collection.find_one({"Uid": uid})
    
    count = len(documents["Entries"])
    # print(count)

    print("Check out your entries below: ")
    if count > 0:
        for i in range(count):
            print(str(i+1)+". Date-Time: " + documents["Entries"][i]["Edatetime"] + "\tYou felt: " + documents["Entries"][i]["Emood"] + "\n\ttype " + str(i+1) + " to view entry\n")

        choice = int(input("Enter the number of the entry you want to view (i -> type 0 to skip): "))
        choice-=1
        if 0 <= choice <= count:
            print("Date-Time: " + documents["Entries"][choice]["Edatetime"] + "\nMood: " + documents["Entries"][choice]["Emood"] + "\nThoughts: " + documents["Entries"][choice]["Ethoughts"])
        elif choice == -1:
            pass
        else:
            print("Invalid choice.\n")
            display(uid)
    else:
        print("No entries found.")

def User(name, result):
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
        
        if (moodRate < 1 or moodRate > 5):
            print("Invalid mood rate. Please enter a number between 1 and 5.")
            moodRate = int(input("How do you feel today? (1-5) (1 = very bad, 5 = very good): "))
        
        newEntry = {"Edatetime" : str(date.today()) + f" @ {time}", "EmoodRate" : moodRate,"Emood" : mood, "Ethoughts" : thoughts}
        collection.update_one({"Uid": uid}, {"$push": {"Entries": newEntry}})
        
        display(uid)
        forward(uid, result)
    elif choice == "n":
        display(uid)
        forward(uid, result)
    else:
        print("Invalid choice.")
