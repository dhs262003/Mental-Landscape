from pymongo import MongoClient
from datetime import date, datetime

client = MongoClient("mongodb://localhost:27017")
db = client["mind_landscape"]
collection = db["userData"]

def tracker(uid, result):
    documents = collection.find_one({"Uid": uid})
    if "Activities" in documents:
        pass
    else:
        collection.update_one({"Uid": uid}, {"$set": {"Activities":[]}})

    while result:
        choice = int(input("1. Add an activity\n2. Mark an activity\n3. View activities\n4. Back\n"))
        
        if choice < 1 or choice > 4:
            print("Invalid choice. Please try again.")
            continue
        
        if choice == 1:
            addActivity(uid)
            pass
        elif choice == 2:
            mrkActivity(uid)
            pass
        elif choice == 3:
            return
        elif choice == 4:
            return


def addActivity(uid):
    print("\nAdd Activity:\n")
    actName = input("Activity name: ")
    tags = input("Tags: ")
    listOTags = list(set(tags.split(",")))

    notes = input("Notes: ")

    while True:
        try:
            due = input("Due date (dd-mm-yyyy): ")
            dueDate = datetime.strptime(due, '%d-%m-%Y').date()
            break
        except ValueError:
            print("Invalid date format. Please try again.")
    dueDate = str(dueDate)

    newAct = {"ActName": actName, "ActTags": listOTags, "ActNotes": notes, "ActDueDate": dueDate}
    collection.update_one({"Uid": uid}, {"$push": {"Activities": newAct}})
    print("\nActivity added successfully.\n")
    return

def mrkActivity(uid):
    print("heelo from mrkActivity")
    print(f"uid: {uid}\n")
    return


tracker("dhso", True)