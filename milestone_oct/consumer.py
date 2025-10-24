import socket
import json
import pandas as pd
import logging
from ETLmodule import run_etl  # Ensure ETLmodule.py with run_etl() exists

processed_path = 'processed_enrollments.csv'

# Required columns for validation and creation
required_columns = [
    "EnrollmentID", "StudentID", "CourseID", "EnrollDate", "Progress",
    "Title", "Category", "Duration", "Name", "Email", "Country"
]

# Set up logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# Ensure CSV exists and contains correct headers
def ensure_csv_valid(path, required_cols):
    try:
        df = pd.read_csv(path)
        if not set(required_cols).issubset(df.columns):
            raise ValueError("CSV missing required columns.")
    except Exception as e:
        logging.warning(f"CSV missing or invalid. Recreating file. Reason: {e}")
        pd.DataFrame(columns=required_cols).to_csv(path, index=False)
        logging.info("Created new processed_enrollments.csv with correct headers.")

# Validating that the new enrollment has all required fields
def validate_enrollment(data, required_fields):
    missing = set(required_fields) - set(data.keys())
    if missing:
        raise ValueError(f"Missing required fields in enrollment: {missing}")

# Starting the socket server
def start_server(host='localhost', port=65432):
    ensure_csv_valid(processed_path, required_columns)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f" Server is listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        with conn:
            data = conn.recv(4096)
            if data:
                try:
                    enrollment = json.loads(data.decode('utf-8'))
                    validate_enrollment(enrollment, required_columns)
                    logging.info(f"Received enrollment: {enrollment['EnrollmentID']}")
                    print(f"Received: {enrollment}")

                    # Read existing data
                    df_existing = pd.read_csv(processed_path)

                    # Append new enrollment
                    new_df = pd.DataFrame([enrollment])
                    updated_df = pd.concat([df_existing, new_df], ignore_index=True)
                    updated_df.to_csv(processed_path, index=False)

                    # Debugging columns before ETL
                    print("Current DataFrame columns:", updated_df.columns.tolist())
                    logging.info(f"DataFrame columns before ETL: {updated_df.columns.tolist()}")

                    # Run ETL
                    run_etl(processed_path)
                    logging.info(f"Enrollment processed and ETL run for: {enrollment['EnrollmentID']}")

                except Exception as e:
                    logging.error(f"Error processing enrollment: {str(e)}")
                    print("Error:", e)

if __name__ == "__main__":
    start_server()
