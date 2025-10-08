from fastapi.testclient import TestClient
from course_api import app

client = TestClient(app)

#test 1

def test_add_course():
    new_course = {
        "id": 2,
        "title": "AI Basic",
        "duration": "60",
        "fee": 5000,
        "is_active": True
    }
    response = client.post("/courses", json=new_course)
    assert response.status_code == 201
    assert response.json()["title"] == "AI Basic"


#test 2
def test_duplicate_course():
    new_course = {
        "id": 1,
        "title": "DL Basic",
        "duration": "90",
        "fee": 9000,
        "is_active": True
    }
    response = client.post("/courses", json=new_course)
    assert response.status_code == 400
    assert response.json()["detail"] == "Course ID already exists"


#test 3
def test_validation_error():
    new_course = { "id": 2, "title": "AI", "duration": 0, "fee": -500, "is_active": True }
    response = client.post("/courses", json=new_course)
    assert response.status_code == 422
    response_text = response.text
    assert "greater_than" in response_text

#test 4

def test_format_error():
    response = client.get("/courses")
    data = response.json()
    assert isinstance(data, list)
    assert all("id" in course for course in data)
    assert all("title" in course for course in data)
    assert all("duration" in course for course in data)
    assert all("fee" in course for course in data)
    assert all("is_active" in course for course in data)

