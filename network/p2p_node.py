import socket
import threading
from network.file_transfer import send_file, receive_file
from network.discovery import get_my_ip

class P2PNode:
    def __init__(self, user):
        self.user = user
        self.port = 5000  # Default port for hosting

    def run(self):
        choice = input("1. Host a session\n2. Join a session\nChoose option: ")
        if choice == "1":
            self.host_session()
        elif choice == "2":
            self.join_session()

    def host_session(self):
        print("Hosting a session...")
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('', self.port))  # Bind to all available interfaces
            server.listen(5)
            print(f"Server is listening on port {self.port}...")
            conn, addr = server.accept()
            print(f"Connection established with {addr}")
            self.handle_connection(conn)
        except Exception as e:
            print(f"An error occurred while hosting: {e}")

    def join_session(self):
        peer_ip = input("Enter peer IP (e.g., 192.168.8.179:5000): ")
        try:
            # Split IP and port
            if ":" not in peer_ip:
                raise ValueError("Invalid IP format. Please use the format IP:PORT.")
            ip, port = peer_ip.split(":")
            port = int(port)

            # Create a socket and connect
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((ip, port))
            print(f"Connected to peer at {ip}:{port}")
            self.handle_connection(conn)
        except ValueError as ve:
            print(ve)
        except socket.gaierror:
            print("Failed to resolve the IP address. Please check the IP and try again.")
        except ConnectionRefusedError:
            print("Connection refused. Ensure the host is running a session and the IP/port are correct.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def handle_connection(self, conn):
        while True:
            print("1. Send File")
            print("2. Receive File")
            print("3. Exit")
            choice = input("Choice: ")
            if choice == '1':
                filename = input("Enter path of file to send: ")
                send_file(conn, filename)
            elif choice == '2':
                receive_file(conn)
            else:
                break
        conn.close()
