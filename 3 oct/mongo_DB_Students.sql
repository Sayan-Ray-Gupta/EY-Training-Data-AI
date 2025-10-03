use university
switched to db university
// Insert one student 
db.student.insertOne({})
{
  acknowledged: true,
  insertedId: ObjectId('68dfa40c7cb033a526e3a265')
}
 db.student.insertOne({
   student_id :1,
   name : "Rahul",
   age : 21 
   city : "Mumbai",
   course: "AI",
   marks : 85
 }
 /insert multuple students
db.student.insertMany([
  { student_id: 2, name: "Priya", age : 22, city :"Delhi", course : "ML", marks: 90},
  { student_id: 3, name: "Arjun", age : 21, city : "bengaluru", course : "Data Science", marks: 78},
  { student_id: 4, name: "Varun", age : 25, city : "Hyderabad", course : "AI", marks: 88},
  { student_id: 5, name: "prity", age : 27, city : "Chennai", course : "ML", marks : 95}
  
])
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('68dfa7997cb033a526e3a267'),
    '1': ObjectId('68dfa7997cb033a526e3a268'),
    '2': ObjectId('68dfa7997cb033a526e3a269'),
    '3': ObjectId('68dfa7997cb033a526e3a26a')
  }
}
// find all students 
db.student.find()
{
  _id: ObjectId('68dfa40c7cb033a526e3a265')
}
{
  _id: ObjectId('68dfa4c17cb033a526e3a266'),
  student_id: 1,
  name: 'Rahul',
  age: 21,
  city: 'Mumbai',
  course: 'AI',
  marks: 85
}
{
  _id: ObjectId('68dfa7997cb033a526e3a267'),
  student_id: 2,
  name: 'Priya',
  age: 22,
  city: 'Delhi',
  course: 'ML',
  marks: 90
}
{
  _id: ObjectId('68dfa7997cb033a526e3a268'),
  student_id: 3,
  name: 'Arjun',
  age: 21,
  city: 'bengaluru',
  course: 'Data Science',
  marks: 78
}
{
  _id: ObjectId('68dfa7997cb033a526e3a269'),
  student_id: 4,
  name: 'Varun',
  age: 25,
  city: 'Hyderabad',
  course: 'AI',
  marks: 88
}
{
  _id: ObjectId('68dfa7997cb033a526e3a26a'),
  student_id: 5,
  name: 'prity',
  age: 27,
  city: 'Chennai',
  course: 'ML',
  marks: 95
}
// find one students 
db.student.findOne ({ name: "Rahul"})
{
  _id: ObjectId('68dfa4c17cb033a526e3a266'),
  student_id: 1,
  name: 'Rahul',
  age: 21,
  city: 'Mumbai',
  course: 'AI',
  marks: 85
}
// find students with marks > 85
db.student.find({ marks: {$gt: 85} })
{
  _id: ObjectId('68dfa7997cb033a526e3a267'),
  student_id: 2,
  name: 'Priya',
  age: 22,
  city: 'Delhi',
  course: 'ML',
  marks: 90
}
{
  _id: ObjectId('68dfa7997cb033a526e3a269'),
  student_id: 4,
  name: 'Varun',
  age: 25,
  city: 'Hyderabad',
  course: 'AI',
  marks: 88
}
{
  _id: ObjectId('68dfa7997cb033a526e3a26a'),
  student_id: 5,
  name: 'prity',
  age: 27,
  city: 'Chennai',
  course: 'ML',
  marks: 95
}
//find only names and courses (projection)
db.student.find({},{name: 1, course: 1, _id : 0})
{}
{
  name: 'Rahul',
  course: 'AI'
}
{
  name: 'Priya',
  course: 'ML'
}
{
  name: 'Arjun',
  course: 'Data Science'
}
{
  name: 'Varun',
  course: 'AI'
}
{
  name: 'prity',
  course: 'ML'
}
//update one student's marks
db.student.updateOne({name :"prity"}, {$set: {marks : 92, course: "Advanced AI"}
                                      })
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
// update many students in course in AI course --> add grade field 
db.student.updateMany(
  { course: "AI"},
  { $set: {grade: "A"}}
)
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 2,
  modifiedCount: 2,
  upsertedCount: 0
}
// Delete one students 
db.student.deleteOne({ name: "Arjun" })
{
  acknowledged: true,
  deletedCount: 1
}
// delete all students with marks < 80
db.student.deleteMany({marks: { $lt: 80 } })
