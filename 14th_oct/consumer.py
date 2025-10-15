# consumer.py
import socket
import threading

def handle_client(conn, addr):
    print(f"[Consumer] Connected by {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        decoded = data.decode()
        print(f"[Consumer] ✅ Task processed for employee ID: {decoded}")
    conn.close()
    print("[Consumer] Connection closed.")

def start_consumer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen()

    print("[Consumer] Waiting for producer to connect...")
    conn, addr = server.accept()

    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()

if __name__ == "__main__":
    start_consumer()
