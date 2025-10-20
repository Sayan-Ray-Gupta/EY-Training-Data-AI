import socket
import json
import pandas as pd
import logging
from ETLmodule import run_etl  # Make sure this file and function exist in the same folder

processed_path = 'processed_enrollments.csv'

# Set up logging
logging.basicConfig(
    filename='log.app',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# Ensuring CSV exists and has correct headers
try:
    df_existing = pd.read_csv(processed_path)
except Exception:
    # If file is missing or invalid, create a new one with headers
    required_columns = [
        "EnrollmentID", "StudentID", "CourseID", "EnrollDate", "Progress",
        "Title", "Category", "Duration", "Name", "Email", "Country"
    ]
    pd.DataFrame(columns=required_columns).to_csv(processed_path, index=False)
    df_existing = pd.read_csv(processed_path)
    logging.info("Created new processed_enrollments.csv with headers.")

# Function to start socket server
def start_server(host='localhost', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"📡 Server is listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        with conn:
            data = conn.recv(4096)
            if data:
                try:
                    enrollment = json.loads(data.decode('utf-8'))
                    logging.info(f"Received enrollment: {enrollment['EnrollmentID']}")
                    print(f"Received: {enrollment}")

                    # Read existing data again in case multiple enrollments are received
                    df_existing = pd.read_csv(processed_path)

                    # Append new enrollment
                    new_df = pd.DataFrame([enrollment])
                    updated_df = pd.concat([df_existing, new_df], ignore_index=True)
                    updated_df.to_csv(processed_path, index=False)

                    # Run the ETL process
                    run_etl(processed_path)
                    logging.info(f"Enrollment processed and ETL run for: {enrollment['EnrollmentID']}")

                except Exception as e:
                    logging.error(f"Error processing enrollment: {str(e)}")
                    print("Error:", e)

if __name__ == "__main__":
    start_server()
