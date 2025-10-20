import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Configure logging to write to 'app.log' file
logging.basicConfig(
    filename="app.log",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

class Course(BaseModel):
    CourseID: str
    Title: str
    Category: str
    Duration: int

df_courses = pd.read_csv("courses.csv")
courses = df_courses.to_dict(orient='records')

@app.get("/courses")
def get_courses():
    return {"courses": courses}

@app.post("/courses", status_code=201)
def add_course(course: Course):
    if any(c['CourseID'] == course.CourseID for c in courses):
        logging.error(f"Attempt to add course with existing CourseID: {course.CourseID}")
        raise HTTPException(status_code=400, detail="CourseID already exists")
    courses.append(course.dict())
    logging.info(f"New course added: {course.CourseID} - {course.Title}")
    return {"message": "Course added successfully", "course": course}

@app.put("/courses/{course_id}")
def update_course(course_id: str, updated_course: Course):
    for i, c in enumerate(courses):
        if c["CourseID"] == course_id:
            courses[i] = updated_course.dict()
            logging.info(f"Course updated: {course_id}")
            return {"message": "Course updated successfully", "course": courses[i]}
    logging.error(f"Update failed - course not found: {course_id}")
    raise HTTPException(status_code=404, detail="Course not found")

@app.delete("/courses/{course_id}")
def delete_course(course_id: str):
    for i, c in enumerate(courses):
        if c["CourseID"] == course_id:
            courses.pop(i)
            logging.info(f"Course deleted: {course_id}")
            return {"message": "Course deleted successfully"}
    logging.error(f"Delete failed - course not found: {course_id}")
    raise HTTPException(status_code=404, detail="Course not found")




#student setup
class Student(BaseModel):
    StudentID: str
    Name: str
    Email: str
    Country: str

df_students = pd.read_csv("students.csv")
students = df_students.to_dict(orient='records')

@app.get("/students")
def get_students():
    return {"students": students}

@app.post("/students", status_code=201)
def add_student(student: Student):
    if any(s['StudentID'] == student.StudentID for s in students):
        logging.error(f"Student already exists: {student.StudentID}")
        raise HTTPException(status_code=400, detail="StudentID already exists")
    students.append(student.dict())
    logging.info(f"Student added: {student.StudentID} - {student.Name}")
    return {"message": "Student added successfully", "student": student}

@app.put("/students/{student_id}")
def update_student(student_id: str, updated_student: Student):
    for i, s in enumerate(students):
        if s["StudentID"] == student_id:
            students[i] = updated_student.dict()
            logging.info(f"Student updated: {student_id}")
            return {"message": "Student updated successfully", "student": students[i]}
    logging.error(f"Update failed - student not found: {student_id}")
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    for i, s in enumerate(students):
        if s["StudentID"] == student_id:
            students.pop(i)
            logging.info(f"Student deleted: {student_id}")
            return {"message": "Student deleted successfully"}
    logging.error(f"Delete failed - student not found: {student_id}")
    raise HTTPException(status_code=404, detail="Student not found")
