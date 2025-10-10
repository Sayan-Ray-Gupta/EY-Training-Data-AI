student = {
    "name" :"alice",
    "age": 22,
    "course" : "AI and ML"
}


print(student.get("age"))

student["grade"] = "A"       #adding element
student["age"] = "23"          #amending element

student.pop("course")  #deleting of element

del student["grade"]
print(student)

