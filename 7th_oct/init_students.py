
from fastapi import FastAPI

#create FastAPI instance
app = FastAPI()

#route endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the fastapi demo!"}

#Path parameter example
@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {"student_id": student_id, "name":"Rahul", "course":"AI"}