from fastapi import FastAPI , HTTPException
from pydantic import BaseModel


#create FastAPI instance
app = FastAPI()

#Pydantic model for validation

class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str


#In-memory database

students = [
    {"id":1, "name": "Rahul", "age": 18, "course": "AI"},
    {"id":2, "name": "priya", "age": 27, "course": "ML"},
]

#-------------GET----------

@app.get("/students")
def get_all_students():
    return {"students": students}



@app.get("/students/{student_id}")
def get_student(student_id: int):
    for s in students:
        if s["id"] == student_id:
            return s
    raise HTTPException(status_code=404, detail="student not found")



#----------POST--------------
@app.post("/students", status_code=201)
def add_student(student: Student):
    students.append(student.dict())
    return{"message": "student added successfully","students": students}





#------------PUT--------------------
@app.put("/students/{student_id}")
def get_student(student_id: int, updated_student: Student):
    for i, s in enumerate(students):
        if s["id"] == student_id:
            students[i] = updated_student.dict()
            return {"message": "student added successfully","student": updated_student}
    raise HTTPException(status_code=404, detail="student not found")




#-----------DELETE-----------

@app.delete("/students/{student_id}")
def delete_student(student_id: int, ):
    for i, s in enumerate(students):
        if s["id"] == student_id:
            students.pop(i)
            return {"message": "Student Deleted Successfully"}
    raise  HTTPException (status_code = 404, detail= "Student not found")