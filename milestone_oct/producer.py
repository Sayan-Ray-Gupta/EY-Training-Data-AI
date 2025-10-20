import socket
import json

def send_enrollment(enrollment_data, host='localhost', port=65432):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            message = json.dumps(enrollment_data)
            s.sendall(message.encode('utf-8'))
            print(f" Sent enrollment: {enrollment_data['EnrollmentID']}")
    except ConnectionRefusedError:
        print(" Cannot connect to the server. Make sure consumer_socket.py is running.")

# Example usage
if __name__ == "__main__":
    sample_enrollment = {
        "EnrollmentID": "E008",
        "StudentID": "S005",
        "CourseID": "C103",
        "EnrollDate": "2025-10-08",
        "Progress": 90,
        "Title": "Data Visualization with Power BI",
        "Category": "Analytics",
        "Duration": 30,
        "Name": "Meena",
        "Email": "meena@example.com",
        "Country": "USA"
    }

    send_enrollment(sample_enrollment)
