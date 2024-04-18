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
            sA = int(input("\n1. View all activities\n2. Put a filter\n"))
            if sA < 1 or sA > 3:
                print("Invalid choice. Please try again.")
                continue
            if sA == 1:
                seeActivity(uid, sA)
                return
            elif sA == 2:
                seeActivity(uid, sA)
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

def checkTags(tag, uid):
    documents = collection.find_one({"Uid": uid})
    for activity in documents['Activities']:
        for tagName in activity['ActTags']:
            if tagName == tag:
                return True
    return False

def seeActivity(uid, choice):
    documents = collection.find_one({"Uid": uid})
    docLen = len(documents['Activities'])
    if choice == 1:
        print("\nAll activities:\n")
        for i in range(docLen):
            print(f"{i+1}. {documents['Activities'][i]['ActName']}\t\tDue Date: {documents['Activities'][i]['ActDueDate']}")
    if choice == 2:
        while True:
            sAfilter = int(input("\nFilters: \n1. Filter by tags\n2. Filter by due date\n"))
            if sAfilter < 1 or sAfilter > 2:
                print("ERROR....\nInvalid choice. Please try again.")
                continue
            else: break
        
        if sAfilter == 1:
            while True:
                tag = input("Enter tag: ")
                if checkTags(tag, uid):
                    print("\nActivities matching the tag:\n")
                    printed_activities = set()
                    idx = 1
                    for activity in documents['Activities']:
                        if tag in activity['ActTags'] and activity['ActName'] not in printed_activities:
                            printed_activities.add(activity['ActName'])  # Add the activity name to the set
                            print(f"{idx}. {activity['ActName']}\t\tDue Date: {activity['ActDueDate']}")
                            idx+=1
                    break
                else:
                    print("ERROR....\nInvalid tag. Please try again.\n")
                    continue
        elif sAfilter == 2:
            print("TODO")
    return

def mrkActivity(uid):
    print("heelo from mrkActivity")
    print(f"uid: {uid}\n")
    return


tracker("dhso", True)