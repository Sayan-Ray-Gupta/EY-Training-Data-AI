# Exercise 1

import json
import logging

from django.contrib.gis.measure import pretty_name

logging.basicConfig(filename='app1.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )
student =[
{"name": "Rahul", "age": 21, "course": "AI", "marks": 85},
{"name": "Priya", "age": 22, "course": "ML", "marks": 90}
]

# write to a json file
with open("student.json", "w") as f:
    json.dump(student, f, indent=4)
    logging.info('student Info saved')
# Read from json file
with open("student.json", "r") as f:
    data = json.load(f)
    logging.info('student Info loaded')
    logging.info(data)


#1. Print all the name of students
for student_name in student:
    print(student_name['name'])

#2 adding the new student info in JSON
new_student = {
    'name':'Ravi',
    "age": 28,
    "course": "Data Science",
    "marks": 98
}
#3 saving the info in json
student.append(new_student)
logging.info('New student info added: Ravi')

#4 reading and writing the info in the previous json file

with open("student.json", "w") as f:
    json.dump(student, f, indent=4)
    logging.info('File saved successfully')
