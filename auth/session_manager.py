class SessionManager:
    def __init__(self):
        self.logged_in_user = None

    def login(self, username):
        self.logged_in_user = username

    def logout(self):
        self.logged_in_user = None

    def is_logged_in(self):
        return self.logged_in_user is not None

    def get_logged_in_user(self):
        return self.logged_in_user
