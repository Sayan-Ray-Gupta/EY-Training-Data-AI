use university
switched to db university
db.teachers.insertOne({
   teachers_id :1,
   name : "Avinash Singh",
   age : 45,
   city : "Bengaluru",
   course : "AI",
   Salary :  45000
 })
 
 db.teachers.insertMany([
  { teachers_id : 102, name: "vikas Mishra", age : 42, city :"Mumbai", course : "AI", salary : 30000},
  { teachers_id : 103, name: "Pallavi Roy", age : 30, city : "Chennai", course : "Data Science", salary: 47000},
  { teachers_id : 104, name: "Rita Garg", age : 48, city : "Delhi", course : "Data Science", salary: 50000},
  { teachers_id : 105, name: "Raman RK", age : 57, city : "Chennai", course : "ML", salary : 35000}
  
])
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('68dfb92f9ef40b64de906d8a'),
    '1': ObjectId('68dfb92f9ef40b64de906d8b'),
    '2': ObjectId('68dfb92f9ef40b64de906d8c'),
    '3': ObjectId('68dfb92f9ef40b64de906d8d')
  }
}
db.teachers.find
[Function: find] AsyncFunction {
  returnsPromise: true,
  apiVersions: [ 1, Infinity ],
  returnType: 'Cursor',
  serverVersions: [ '0.0.0', '999.999.999' ],
  topologies: [ 'ReplSet', 'Sharded', 'LoadBalanced', 'Standalone' ],
  deprecated: false,
  platforms: [ 'Compass', 'Browser', 'CLI' ],
  isDirectShellCommand: false,
  acceptsRawInput: false,
  shellCommandCompleter: undefined,
  newShellCommandCompleter: undefined,
  help: [Function (anonymous)] Help
}
db.teachers.find()
{
  _id: ObjectId('68dfb3dd9ef40b64de906d85'),
  teachers_id: 1,
  name: 'Avinash Singh',
  age: 45,
  city: 'Bengaluru',
  course: 'AI',
  Salary: 45000
}
{
  _id: ObjectId('68dfb92f9ef40b64de906d8a'),
  teachers_id: 102,
  name: 'vikas Mishra',
  age: 42,
  city: 'Mumbai',
  course: 'AI',
  salary: 30000
}
{
  _id: ObjectId('68dfb92f9ef40b64de906d8b'),
  teachers_id: 103,
  name: 'Pallavi Roy',
  age: 30,
  city: 'Chennai',
  course: 'Data Science',
  salary: 47000
}
{
  _id: ObjectId('68dfb92f9ef40b64de906d8c'),
  teachers_id: 104,
  name: 'Rita Garg',
  age: 48,
  city: 'Delhi',
  course: 'Data Science',
  salary: 50000
}
{
  _id: ObjectId('68dfb92f9ef40b64de906d8d'),
  teachers_id: 105,
  name: 'Raman RK',
  age: 57,
  city: 'Chennai',
  course: 'ML',
  salary: 35000
}
// find teacher with salary above 30000
db.teachers.find({ salary: {$gt: 30000} })
{
  _id: ObjectId('68dfb92f9ef40b64de906d8b'),
  teachers_id: 103,
  name: 'Pallavi Roy',
  age: 30,
  city: 'Chennai',
  course: 'Data Science',
  salary: 47000
}
{
  _id: ObjectId('68dfb92f9ef40b64de906d8c'),
  teachers_id: 104,
  name: 'Rita Garg',
  age: 48,
  city: 'Delhi',
  course: 'Data Science',
  salary: 50000
}
{
  _id: ObjectId('68dfb92f9ef40b64de906d8d'),
  teachers_id: 105,
  name: 'Raman RK',
  age: 57,
  city: 'Chennai',
  course: 'ML',
  salary: 35000
}
// update the teacher id of Avinash
db.teachers.updateOne({name :"Avinash Singh"}, {$set: {teachers_id : 101, salary: 47000}
                                      })
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
// deleting the records of Ml teacher
db.teachers.deleteMany({course: { $lt: 'ML' } })
