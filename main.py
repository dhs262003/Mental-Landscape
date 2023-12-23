from login import Login
from signup import Signup

print("Welcome to Mental Landscape!")
options = int(input("1. Login\n2. Sign up\n3. Exit\n"))

if options == 1:
    result = Login()
    if result["success"]:
        print(f"Login successful!\nWelcome, {result['username']}!")
        username = result["username"]
    else:
        print("Invalid username or password.")
        print("Please try again.\n")
elif options == 2:
    Signup()
elif options == 3:
    exit()
