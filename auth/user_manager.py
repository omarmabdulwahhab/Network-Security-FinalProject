import json
import os

class UserManager:
    def __init__(self):
        self.user_file = 'storage/users.json'
        os.makedirs(os.path.dirname(self.user_file), exist_ok=True)
        if not os.path.exists(self.user_file):
            with open(self.user_file, 'w') as f:
                json.dump([], f)

    def register_user(self):
        username = input("Enter new username: ")
        password = input("Enter password: ")

        # Load existing users
        try:
            with open(self.user_file, 'r') as f:
                users = json.load(f)
        except json.JSONDecodeError:
            users = []

        # Check if username already exists
        if any(user['username'] == username for user in users):
            print("Username already exists. Please try again.")
            return

        # Add new user
        users.append({'username': username, 'password': password})
        with open(self.user_file, 'w') as f:
            json.dump(users, f)

        print("User registered successfully!")

    def login_user(self):
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Load existing users
        try:
            with open(self.user_file, 'r') as f:
                users = json.load(f)
        except json.JSONDecodeError:
            print("No users found. Please register first.")
            return None

        # Check if the username and password match
        for user in users:
            if user['username'] == username and user['password'] == password:
                print("Login successful!")
                return user

        print("Invalid username or password. Please try again.")
        return None
