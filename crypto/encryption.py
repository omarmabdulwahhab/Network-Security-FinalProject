from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import os


SYMMETRIC_KEY = hashlib.sha256(b"shared_secret_key").digest()  

def encrypt_file(file_path):
    """Encrypts a file using AES."""
    encrypted_file_path = file_path + ".enc"
    cipher = AES.new(SYMMETRIC_KEY, AES.MODE_CBC)
    iv = cipher.iv  

    with open(file_path, 'rb') as f:
        plaintext = f.read()

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    with open(encrypted_file_path, 'wb') as f:
        f.write(iv + ciphertext)  

    return encrypted_file_path 

def decrypt_file(encrypted_file_path):
    """Decrypts a file using AES."""
    print(f"Decrypting file: {encrypted_file_path}")
    decrypted_file_path = encrypted_file_path.replace(".enc", ".dec")

    try:
        with open(encrypted_file_path, 'rb') as f:
            iv = f.read(16)  
            print(f"Read IV: {iv}")
            ciphertext = f.read()
            print(f"Read ciphertext of size: {len(ciphertext)}")

        cipher = AES.new(SYMMETRIC_KEY, AES.MODE_CBC, iv=iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        print("Decryption successful!")

        with open(decrypted_file_path, 'wb') as f:
            f.write(plaintext)
        print(f"Decrypted file saved as: {decrypted_file_path}")

        return decrypted_file_path
    except Exception as e:
        print(f"An error occurred during decryption: {e}")
        raise

def generate_file_hash(file_path):
    """Generates a SHA-256 hash for a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def receive_file(self, conn):
    """Receive and decrypt a file from the peer."""
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

def send_file(self, file_path, conn):
    """Encrypt and send a file to the peer."""
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