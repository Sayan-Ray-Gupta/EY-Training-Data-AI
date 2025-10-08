from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test 1
def test_get_all_employees():
    response = client.get("/employees") # ACT
    assert response.status_code == 200 # Assert
    assert isinstance(response.json(), dict) # Assert

# Test 2
def test_add_employee():
    new_emp = {
        "id": 2,
        "name": "Neha Verma",
        "dept": "Software Engineering",
        "salary": 50000
    }
    response = client.post("/employees", json=new_emp)
    assert response.status_code == 201
    assert response.json()["name"] == "Neha Verma"


# Test 3
def test_get_employee_by_id():
    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json()["name"] == "RaONE"


# Test 4
def test_get_employee_not_found():
    response = client.get("/employees/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"



#test 5
def test_update_employee():
    up_new_emp = {"id": 1, "name": "Verma", "dept": "Gaming", "salary": 45000.00}
    response = client.put("/employees/2", json=up_new_emp)
    assert response.status_code == 200
    assert response.json()["name"] == "Verma"


#test 6
def test_delete_employee():
    response = client.delete("/employees/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Employee Deleted Successfully"