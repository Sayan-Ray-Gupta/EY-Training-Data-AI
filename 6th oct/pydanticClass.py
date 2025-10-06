from pydantic import BaseModel

#define a model like schema of sql
class Student(BaseModel):
    name: str
    age: int
    email: str
    is_active : bool = True


#valid data
data = {"name": "Aisha","age": 29, "email": "aisha@abc.com" }
student = Student(**data)

print(student)
print(student.name)

