import json

# python dictionary
student = {
    "Name": "Rahul",
    "age" : 21,
    "course" : ["AI","ML"],
    "marks" : {"AI": 85 , "ML" : 90 }

}
print(student)
# write to a json file
with open("student.json", "w") as f:
    json.dump(student, f, indent=4)

# Read from json file
with open("student.json", "r") as f:
    data = json.load(f)

print(data["Name"])
print(data["marks"]["AI"])
print(data["marks"]["ML"])