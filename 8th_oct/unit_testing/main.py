from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Pydantic model
class Employee(BaseModel):
    id: int
    name: str
    dept: str
    salary: float

# in-memory database
employees = [
    {"id": 1, "name": "RaONE", "dept": "Gaming", "salary": 45000.00}
]
# GET a single record
@app.get("/employees/{emp_id}")
def get_employee(emp_id: int):
    for record in employees:
        if record["id"] == emp_id:
            return record
    raise HTTPException(status_code=404, detail="Employee not found")


# GET all request
@app.get("/employees")
def get_all():
    return {"Employees": employees}


# POST a record
@app.post("/employees", status_code=201)
def add_employee(employee: Employee):
    present_ids = []
    for record in employees:
        present_ids.append(record["id"])
    if employee.dict()["id"] not in present_ids:
        employees.append(employee.dict())
        return employee
    else:
        raise HTTPException(status_code=404, detail="Employee already exists")

# PUT request
@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, updated_employee: Employee):
    for i, record in enumerate(employees):
        if record["id"] == emp_id:
            employees[i] = updated_employee.dict()
            return employees[i]
    raise HTTPException(status_code=404, detail="Employee not found")


# DELETE Request
@app.delete("/employees/{emp_id}")
def delete_student(emp_id: int):
    for i, s in enumerate(employees):
        if s["id"] == emp_id:
            employees.pop(i)
            return {"message": "Employee Deleted Successfully"}
    raise HTTPException(status_code=404, detail="Employee not found")
