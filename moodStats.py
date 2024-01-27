from pymongo import MongoClient
from datetime import date, datetime

client = MongoClient("mongodb://localhost:27017")
db = client["mind_landscape"]
collection = db["userData"]

def comments(name, num, per, moodType):
    uid = name
    num = num
    per = per
    moodType = moodType
    documents = collection.find_one({"Uid": uid})
    time = str(datetime.now().time().isoformat(timespec='minutes'))

    if "AvgMood" in documents:
        pass
    else:
        collection.update_one({"Uid": uid}, {"$set": {"AvgMood":[]}})

    if moodType == "Very bad":
        print("\nHeres something that might brighten your day.\n'Winning doesn’t always mean being first. Winning means you’re doing better than you’ve done before.'")
        newEntry = {"Mdatetime" : str(date.today()) + f" @ {time}", "Curr_AvgMoodType" : moodType,"Curr_AvgMoodNum" : num, "Curr_AvgMoodPercent" : per}
    elif moodType == "Bad":
        print("\nHeres something that might put a smile on your face.\n'The struggle you’re in today is developing the strength you need tomorrow.'")
        newEntry = {"Mdatetime" : str(date.today()) + f" @ {time}", "Curr_AvgMoodType" : moodType,"Curr_AvgMoodNum" : num, "Curr_AvgMoodPercent" : per}
    elif moodType == "Average":
        print("\nHeres something that might show you are on track of wining LIFE.\n'The best way to predict the future is to invent it.'")
        newEntry = {"Mdatetime" : str(date.today()) + f" @ {time}", "Curr_AvgMoodType" : moodType,"Curr_AvgMoodNum" : num, "Curr_AvgMoodPercent" : per}
    elif moodType == "Good":
        print("\nHeres something that might keep you motivated.\n'Live life to the fullest and focus on the positive.'")
        newEntry = {"Mdatetime" : str(date.today()) + f" @ {time}", "Curr_AvgMoodType" : moodType,"Curr_AvgMoodNum" : num, "Curr_AvgMoodPercent" : per}
    elif moodType == "Very good":
        print("\nHeres something that will keep you in high sprits.\n'The greatest glory in life is not in never falling, but in rising every time we fall.'")
        newEntry = {"Mdatetime" : str(date.today()) + f" @ {time}", "Curr_AvgMoodType" : moodType,"Curr_AvgMoodNum" : num, "Curr_AvgMoodPercent" : per}
    
    collection.update_one({"Uid": uid}, {"$push": {"AvgMood": newEntry}})
    print("")


def stats(name):
    uid = name
    documents = collection.find_one({"Uid": uid})
    
    count = len(documents["Entries"])
    storedMrate = []

    if count>4:
        for i in range(count):
            storedMrate.append(documents["Entries"][i]["EmoodRate"])
        # print(storedMrate)
        pFive = (storedMrate.count(5)/count)*100
        pFour = (storedMrate.count(4)/count)*100
        pThree = (storedMrate.count(3)/count)*100
        pTwo = (storedMrate.count(2)/count)*100
        pOne = (storedMrate.count(1)/count)*100
        
        print("5: " + str(pFive) + "%\n4: " + str(pFour) + "%\n3: " + str(pThree) + "%\n2: " + str(pTwo) + "%\n1: " + str(pOne) + "%")
        
        percentage = [pFive, pFour, pThree, pTwo, pOne]
        print("\n\nYour Most visited mood is : ")
        if pFive == max(percentage):
            print("5(i.e. very good mood) which was recorded " + str(max(percentage)) + "%" + " of times")
            comments(uid, 5, max(percentage), "Very good")
        elif pFour == max(percentage):
            print("4(i.e. good mood) which was recorded " + str(max(percentage)) + "%" + " of times")
            comments(uid, 4, max(percentage), "Good")
        elif pThree == max(percentage):
            print("3(i.e. average mood) which was recorded " + str(max(percentage)) + "%" + " of times")
            comments(uid, 3, max(percentage), "Average")
        elif pTwo == max(percentage):
            print("2(i.e. bad mood) which was recorded " + str(max(percentage)) + "%" + " of times")
            comments(uid, 2, max(percentage), "Bad")
        elif pOne == max(percentage):
            print("1(i.e. very bad mood) which was recorded " + str(max(percentage)) + "%" + " of times")
            comments(uid, 1, max(percentage), "Very bad")

    else:
        print("Can't calculate mood statistics for less than 5 entries.\nMake sure you have at least 5 entries.")

# stats("dhso")