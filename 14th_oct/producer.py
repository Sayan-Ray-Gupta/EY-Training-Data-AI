# producer.py
import socket
import time


def start_producer():
    employees = [
        {"id": 101, "name": "Alice"},
        {"id": 102, "name": "Bob"},
    ]

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 9999))
        print("[Producer] Connected to consumer.")

        for emp in employees:
            message = str(emp['id'])
            print(f"[Producer] Sending task for employee ID: {emp['id']}, Name: {emp['name']}")
            client.send(message.encode())
            time.sleep(1)

    except ConnectionRefusedError:
        print("[Producer] Could not connect to consumer. Is it running?")
    finally:
        client.close()
        print("[Producer] Finished sending tasks.")


if __name__ == "__main__":
    start_producer()
