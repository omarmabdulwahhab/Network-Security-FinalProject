import json
import os
import hashlib

class UserManager:
    def __init__(self):
        self.user_file = 'storage/users.json'
        os.makedirs(os.path.dirname(self.user_file), exist_ok=True)
        if not os.path.exists(self.user_file):
            # Initialize the file as an empty dictionary
            with open(self.user_file, 'w') as f:
                json.dump({}, f)
        else:
            # Ensure the file is a dictionary
            with open(self.user_file, 'r') as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, dict):
                        raise ValueError("Invalid file format. Reinitializing as an empty dictionary.")
                except (json.JSONDecodeError, ValueError):
                    with open(self.user_file, 'w') as f:
                        json.dump({}, f)

    def register_user(self):
        username = input("Enter new username: ")
        password = input("Enter password: ")

        # Load existing users
        with open(self.user_file, 'r') as f:
            users = json.load(f)

        # Check if username already exists
        if username in users:
            print("Username already exists. Please try again.")
            return

        # Hash the password with SHA-256
        salt = os.urandom(16).hex()  # Generate a random salt
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()

        # Add the new user to the dictionary
        users[username] = {'hash': hashed, 'salt': salt}

        # Save the updated users back to the file
        with open(self.user_file, 'w') as f:
            json.dump(users, f)

        print("User registered successfully!")

    def login_user(self):
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Load existing users
        with open(self.user_file, 'r') as f:
            users = json.load(f)

        # Check if the username exists
        if username not in users:
            print("Invalid username or password.")
            return None

        # Verify the password
        user_record = users[username]
        hashed = hashlib.sha256((password + user_record['salt']).encode()).hexdigest()
        if hashed == user_record['hash']:
            print("Login successful!")
            return username
        else:
            print("Invalid username or password.")
            return None
