CREATE database Schooldb;

-- use this database
use Schooldb;

create table students (
	id int auto_increment primary key,
    name varchar (50),
    age int,
    course varchar (50),
    marks int 
    );
    
-- inserting rows 
insert into students (name, age, course, marks)
values ('priya', 22, 'ML', 90),
	('alex', 30, 'DL', 78),
    ('rahul', 21, 'AI', 88),
    ('yash', 25, 'finance','92');
    
    
-- Select all
select * from students;


-- select specific column 
Select name , marks From students;

-- Filter with WHERE

select * from students where marks > 80 ;

-- UPDATE 

update students
SET marks = 95, course = 'Advance AI'
where id = 3 ;

-- update students SET course = 'AI';

-- delete 

delete from students where id = 2 ;


-- these are CRUD (create, read, update, delete ) operation