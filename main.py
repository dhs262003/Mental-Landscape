from login import Login
from signup import Signup
from user import User

def runner():
    options = int(input("1. Login\n2. Sign up\n3. Exit\n"))
    if options == 1:
        result = Login()
        if result["success"]:
            print(f"Login successful!")
            username = result["username"]
            User(username)
        else:
            print("Invalid username or password.")
            print("Please try again.\n")
            runner()
    elif options == 2:
        Signup()
        runner()
    elif options == 3:
        exit()


print("Welcome to Mental Landscape!")
runner()