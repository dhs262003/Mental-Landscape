def Signup():
    username = input("Choose a username: ")
    if len(username) < 4:
        print("Username should be at least 4 characters long.")
        return
    with open("passwords.txt", "r") as file:
        for line in file:
            stored_username, _ = line.strip().split(":")
            if username == stored_username:
                print("Username already exists, please choose a different username.")
                return
    password = input("Choose a password: ")
    if len(password) < 8:
        print("Password should be at least 8 characters long.")
        return
    # users[username] = password
    print("Sign up successful!")
    with open("passwords.txt", "a") as file:
        file.write(f"\n{username}:{password}")