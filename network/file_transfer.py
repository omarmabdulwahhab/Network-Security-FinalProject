import os
import json

CHUNK_SIZE = 4096

def send_file(conn, filename):
    if not os.path.exists(filename):
        conn.send(b"ERROR")
        return

    filesize = os.path.getsize(filename)
    conn.send(json.dumps({'status': 'OK', 'filename': filename, 'filesize': filesize}).encode())

    with open(filename, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            conn.send(chunk)
    print("File sent.")

def receive_file(conn, download_dir='downloads'):
    os.makedirs(download_dir, exist_ok=True)
    metadata = json.loads(conn.recv(1024).decode())

    if metadata.get('status') != 'OK':
        print("File not available.")
        return

    filename = os.path.basename(metadata['filename'])
    filesize = metadata['filesize']
    filepath = os.path.join(download_dir, filename)

    with open(filepath, 'wb') as f:
        total_received = 0
        while total_received < filesize:
            data = conn.recv(CHUNK_SIZE)
            f.write(data)
            total_received += len(data)

    print(f"File received and saved to {filepath}")
