use schooldb ;

create table Teachers (
	teacher_id int auto_increment primary key,
    name varchar (50),
    subject_id int
);

create table Subjects (
	subject_id int auto_increment primary key,
    subject_name varchar(50)
);

INSERT INTO Subjects (subject_name) VALUES
('Mathematics'),   -- id = 1
('Science'),       -- id = 2
('English'),       -- id = 3
('History'),       -- id = 4
('Geography');     -- id = 5 (no teacher yet)

INSERT INTO Teachers (name, subject_id) VALUES
('Rahul Sir', 1),   -- Mathematics
('Priya Madam', 2), -- Science
('Arjun Sir', NULL),-- No subject assigned
('Neha Madam', 3);  -- English


select t.name, s.subject_name 
FROM Teachers t
inner join Subjects s
ON t.subject_id = s.subject_id;



select t.name, s.subject_name 
FROM Teachers t
left join Subjects s
ON t.subject_id = s.subject_id;



select t.name, s.subject_name 
FROM Teachers t
right join Subjects s
ON t.subject_id = s.subject_id;



select t.name, s.subject_name 
FROM Teachers t
left join Subjects s
ON t.subject_id = s.subject_id

union 


select t.name, s.subject_name 
FROM Teachers t
right join Subjects s
ON t.subject_id = s.subject_id;