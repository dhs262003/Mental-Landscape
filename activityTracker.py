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
        choice = int(input("\n1. Add an activity\n2. Mark an activity\n3. View activities\n4. Back\n"))
        
        if choice < 1 or choice > 4:
            print("Invalid choice. Please try again.")
            continue
        
        if choice == 1:
            addActivity(uid)
            pass
        elif choice == 2:
            mrkActivity(uid, True)
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

    newAct = {"ActName": actName, "ActTags": listOTags, "ActNotes": notes, "ActDueDate": dueDate, "ActDone": False}
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
    if choice == 1:  # View all activities
        mrkActivity(uid, False)
    if choice == 2:  # Filter activities
        while True:
            sAfilter = int(input("\nFilters: \n1. Filter by tags\n2. Filter by due date\n"))
            if sAfilter < 1 or sAfilter > 2:
                print("ERROR....\nInvalid choice. Please try again.")
                continue
            else: break
        
        if sAfilter == 1: # Filter by tags
            while True:
                tag = input("Enter tag: ")
                if checkTags(tag, uid):
                    print("\nActivities matching the tag:\n")
                    printed_activities = set()
                    idx = 1
                    for activity in documents['Activities']:
                        if tag in activity['ActTags'] and activity['ActName'] not in printed_activities:
                            printed_activities.add(activity['ActName'])  # Add the activity name to the set
                            done = "Activity Done" if activity['ActDone'] else "Activity Not done"
                            print(f"{idx}. {activity['ActName']}\t\tDue Date: {activity['ActDueDate']}\t\t{done}")
                            idx+=1
                    break
                else:
                    print("ERROR....\nInvalid tag. Please try again.\n")
                    continue
        elif sAfilter == 2: # Filter by due date
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            overDueActivities = []
            onTimeActivities = []
            for activity in documents['Activities']:
                duedate = activity['ActDueDate']
                dDateObj = datetime.strptime(duedate, "%Y-%m-%d")
                if dDateObj < today: overDueActivities.append((activity, duedate))
                else: onTimeActivities.append((activity, duedate))
            
            print("\nOverdue Activities:")
            for activity, duedate in overDueActivities:
                done = "Activity Done" if activity['ActDone'] else "Activity Not done"
                print(f"{activity['ActName']} \t- Due Date: {duedate} \t- {done}")
            
            print("\nActivities with Time Left:")
            for activity, duedate in onTimeActivities:
                done = "Activity Done" if activity['ActDone'] else "Activity Not done"
                timeLeft = dDateObj - today
                print(f"{activity['ActName']} \t- Due Date: {duedate} \t- {timeLeft.days} days left \t- {done}")
    return

def updateActivity(uid, idx):
    documents = collection.find_one({"Uid": uid})
    print(f"\nUpdate Activity:\n{idx+1}")
    print("\nWhich value to update?\n1. Activity name\n2. Tags\n3. Notes\n4. Due date\n")
    while True: #Taking the choice
        choice = int(input("Enter your choice: "))
        if choice < 1 or choice > 4:
            print("Invalid choice. Please try again.")
            continue
        else: break
    if choice == 1: # update activity name
        while True: # enter new name
            newActName = input("Enter new activity name: ")
            if newActName != "" and newActName != documents['Activities'][idx]['ActName'] and newActName!= " ":
                collection.update_one({"Uid": uid}, {"$set": {f"Activities.{idx}.ActName": newActName}})
                print(f"\nActivity name updated to '{newActName}'.\n")
                break
            else:
                print("\nInvalid name. Please try again.\n")
                continue
    elif choice == 2: # update tags
        listOfTags = documents['Activities'][idx]['ActTags']
        while True:
            newTag = input("Enter new tag: ")
            if newTag != "" and newTag not in listOfTags and newTag != " ":
                listOfTags.append(newTag)
                collection.update_one({"Uid": uid}, {"$set": {f"Activities.{idx}.ActTags": listOfTags}})
                print(f"\nTag '{newTag}' added to activity.\n")
                break
            else:
                print("\nInvalid tag. Please try again.\n")
                continue
    elif choice == 3: # update notes
        while True:
            newActNote = input("Enter new activity notes: ")
            if newActNote != "" and newActNote != documents['Activities'][idx]['ActNotes']:
                collection.update_one({"Uid": uid}, {"$set": {f"Activities.{idx}.ActNotes": newActNote}})
                print(f"\nActivity notes updated.\n")
                break
            else:
                print("\nInvalid values in new notes. Please try again.\n")
                continue
    elif choice == 4: # update due date
        while True:
            newActDueDate = input("Enter new activity due date (dd-mm-yyyy): ")
            while True:
                try:
                    newActDueDate = datetime.strptime(newActDueDate, '%d-%m-%Y').date()
                    break
                except ValueError:
                    print("Invalid date format. Please try again.")
            
            newActDueDate = str(newActDueDate)
            if newActDueDate != documents['Activities'][idx]['ActDueDate']:
                collection.update_one({"Uid": uid}, {"$set": {f"Activities.{idx}.ActDueDate": newActDueDate}})
                print(f"\nActivity due date updated to '{newActDueDate}'.\n")
                break
            else:
                print("\nEnter a different due date. Please try again.\n")
                continue

    return

def mrkActivity(uid, change):
    documents = collection.find_one({"Uid": uid})
    print("\nAll activities:\n")
    for i in range(len(documents['Activities'])):
        print(f"{i+1}. {documents['Activities'][i]['ActName']}\t\tDue Date: {documents['Activities'][i]['ActDueDate']}\t\tDone: {documents['Activities'][i]['ActDone']}")
    
    while change: # mrk or update ?
        what = int(input("\nSelect the following:\n1. Mark an activity as done\n2. update an activity\n"))
        if what < 1 or what > 2:
            print("Invalid choice. Please try again.")
            continue
        else: break
    if change and what == 1: # mark as done
        while True: # enter idx
            idx = int(input("\nEnter the index of the activity to mark as done: "))
            if idx < 1 or idx > len(documents['Activities']):
                print("Invalid choice. Please try again.")
                continue
            else: break
        
        collection.update_one({"Uid": uid}, { "$set": {f"Activities.{(idx-1)}.ActDone": True }})
        print("Activity marked as done.")

    elif change and what == 2: # update
        while True: # enter idx
            idx = int(input("\nEnter the index of the activity to update: "))
            if idx < 1 or idx > len(documents['Activities']):
                print("Invalid choice. Please try again.")
                continue
            else: break
        updateActivity(uid, idx-1)
    return
