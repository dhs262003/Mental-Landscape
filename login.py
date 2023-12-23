def Login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    with open("passwords.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line:
                stored_username, stored_password = line.split(":")
                if username == stored_username and password == stored_password:
                    return {"success": True, "username": stored_username}
    return {"success": False, "username": None}