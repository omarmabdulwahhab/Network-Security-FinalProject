# network/p2p_node.py
import socket
from crypto.encryption import encrypt_file, decrypt_file, generate_file_hash

class P2PNode:
    def __init__(self, username):
        self.username = username
        self.server_socket = None
        self.peer_socket = None
        self.peer_address = None
        self.port = 5000

    def run(self):
        choice = input("1. Host a session\n2. Join a session\nChoose option: ")
        if choice == "1":
            self.host_session()
        elif choice == "2":
            self.join_session()
        else:
            print("Invalid choice. Returning to main menu.")

    def host_session(self):
        print("Hosting a session...")
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('', self.port))
            self.server_socket.listen(1)
            print(f"Server is listening on port {self.port}...")
            conn, addr = self.server_socket.accept()
            print(f"Connection established with {addr}")
            self.handle_peer_connection(conn)
        except Exception as e:
            print(f"An error occurred while hosting: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def join_session(self):
        peer_input = input("Enter peer IP and port (e.g., 192.168.8.179:5000): ")
        try:
            if ":" not in peer_input:
                raise ValueError("Invalid format. Please use the format IP:PORT.")
            peer_ip, peer_port = peer_input.split(":")
            peer_port = int(peer_port)
            self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.peer_socket.connect((peer_ip, peer_port))
            print(f"Connected to peer at {peer_ip}:{peer_port}")
            self.handle_peer_connection(self.peer_socket)
        except ValueError as ve:
            print(ve)
        except socket.gaierror:
            print("Failed to resolve the IP address. Please check the IP and try again.")
        except ConnectionRefusedError:
            print("Connection refused. Ensure the host is running a session and the IP/port are correct.")
        except Exception as e:
            print(f"An error occurred while joining: {e}")
        finally:
            if self.peer_socket:
                self.peer_socket.close()

    def handle_peer_connection(self, conn):
        while True:
            action = input("1. Send a file\n2. Receive a file\n3. Exit\nChoose option: ")
            if action == "1":
                file_path = input("Enter the path of the file to send: ")
                self.send_file(file_path, conn)
            elif action == "2":
                self.receive_file(conn)
            elif action == "3":
                print("Exiting session.")
                break
            else:
                print("Invalid option. Please try again.")

    def send_file(self, file_path, conn):
        try:
            encrypted_file = encrypt_file(file_path)
            file_hash = generate_file_hash(file_path)
            conn.sendall(file_hash.encode())
            print(f"Sent file hash: {file_hash}")
            with open(encrypted_file, 'rb') as f:
                while chunk := f.read(1024):
                    conn.sendall(chunk)
            conn.sendall(b"EOF")
            print(f"Sent encrypted file: {file_path}")
        except Exception as e:
            print(f"An error occurred while sending the file: {e}")

    def receive_file(self, conn):
        try:
            print("Waiting to receive file...")
            received_hash = conn.recv(64).decode()
            print(f"Received file hash: {received_hash}")
            encrypted_file_path = "received_file.enc"
            with open(encrypted_file_path, 'wb') as f:
                while True:
                    chunk = conn.recv(1024)
                    if chunk.endswith(b"EOF"):
                        f.write(chunk[:-3])
                        break
                    f.write(chunk)
                    print(f"Received chunk of size: {len(chunk)}")
            print(f"Encrypted file received and saved as: {encrypted_file_path}")
            print("Starting decryption...")
            decrypted_file_path = decrypt_file(encrypted_file_path)
            print(f"Decrypted file saved as: {decrypted_file_path}")
            calculated_hash = generate_file_hash(decrypted_file_path)
            if calculated_hash == received_hash:
                print("File integrity verified!")
            else:
                print("File integrity verification failed!")
        except Exception as e:
            print(f"An error occurred while receiving the file: {e}")
