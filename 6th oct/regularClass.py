# just a normal Python class
class Student :
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

data = {"name": "Jack", "age": "twenty", "email": "jack@123.com"}
student = Student(**data)


print(student.age)     #doesn't matter the data type, In class age can be a string also