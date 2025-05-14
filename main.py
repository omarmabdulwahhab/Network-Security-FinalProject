# main.py
import os
from auth.user_manager import UserManager
from auth.session_manager import SessionManager
from network.p2p_node import P2PNode
from shared.utils import menu

def run():
    user_manager = UserManager()
    session_manager = SessionManager()

    while True:
        choice = menu([
            "Register",
            "Login",
            "Start P2P Node (Host/Join)",
            "Logout",
            "Exit"
        ])

        if choice == 1:
            user_manager.register_user()
        elif choice == 2:
            user = user_manager.login_user()
            if user:
                session_manager.login(user)
        elif choice == 3:
            if not session_manager.is_logged_in():
                print("You must be logged in to start the node.")
                continue
            node = P2PNode(session_manager.get_logged_in_user())
            node.run()
        elif choice == 4:
            session_manager.logout()
            print("Logged out successfully.")
        else:
            print("Goodbye!")
            break

if __name__ == '__main__':
    os.makedirs('storage', exist_ok=True)
    run()
