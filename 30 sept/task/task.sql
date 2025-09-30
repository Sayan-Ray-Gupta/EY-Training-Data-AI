CREATE DATABASE UniversityDB;
USE UniversityDB;
-- Students Table
CREATE TABLE Students (
student_id INT PRIMARY KEY,
name VARCHAR(50),
city VARCHAR(50)
);
-- Courses Table
CREATE TABLE Courses (
course_id INT PRIMARY KEY,
course_name VARCHAR(50),
credits INT
);
-- Enrollments Table
CREATE TABLE Enrollments (
enroll_id INT PRIMARY KEY,
student_id INT,
course_id INT,
grade CHAR(2),
FOREIGN KEY (student_id) REFERENCES Students(student_id),
FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);
-- Insert Students
INSERT INTO Students VALUES
(1, 'Rahul', 'Mumbai'),
(2, 'Priya', 'Delhi'),
(3, 'Arjun', 'Bengaluru'),
(4, 'Neha', 'Hyderabad'),
(5, 'Vikram', 'Chennai');
-- Insert Courses
INSERT INTO Courses VALUES
(101, 'Mathematics', 4),
(102, 'Computer Science', 3),
(103, 'Economics', 2),
(104, 'History', 3);
-- Insert Enrollments
INSERT INTO Enrollments VALUES
(1, 1, 101, 'A'),
(2, 1, 102, 'B'),
(3, 2, 103, 'A'),
(4, 3, 101, 'C'),

(5, 4, 102, 'B'),
(6, 5, 104, 'A');



-- Level 1
-- Create a stored procedure to list all students.
 
delimiter $$
create procedure all_students()
begin
	select name from students;
end$$
 
delimiter ;
call all_students;


-- Create a stored procedure to list all courses.
 
delimiter $$
create procedure all_course()
begin
	select course_name from courses;
end$$
 
delimiter ;

call all_course;


-- Create a stored procedure to find all students from a given city (take city as input).
 
delimiter $$
create procedure student_city(in city_name varchar(50))
begin
	select name from students where city = city_name;
end$$
 
delimiter ;
call student_city('Mumbai');


-- LEVEL 2
-- Create a stored procedure to list students with their enrolled courses.
 
delimiter $$
create procedure student_course()
begin
	select s.name, c.course_name
    from enrollments e
    join students s on e.student_id = s.student_id
    join courses c on e.course_id = c.course_id;
end$$
 
delimiter ;
call student_course;

-- Create a stored procedure to list all students enrolled in a given course (take course_id as input).
 
delimiter $$
create procedure student_in_course(in course_n varchar(50))
begin
	select s.name, c.course_name
    from enrollments e
    join students s on e.student_id = s.student_id
    join courses c on e.course_id = c.course_id
    where c.course_name = course_n;
end
 
delimiter ;
call student_in_course('History');


-- Create a stored procedure to count the number of students in each course.
 
delimiter $$
create procedure count_of_students()
begin
	select c.course_name, count(e.course_id) as No_of_Students
    from enrollments e
    join courses c on e.course_id = c.course_id
    group by c.course_name, e.course_id;
end$$
delimiter ;
call count_of_students;

-- LEVEL 3
-- Create a stored procedure to list students with course names and grades
 
delimiter $$
create procedure student_course_grades()
begin
	select s.name, c.course_name, e.grade
	from enrollments e
	join students s on e.student_id = s.student_id
    join courses c on e.course_id = c.course_id;
end$$
 
delimiter ;
call student_course_grades;


-- Create a stored procedure to show all courses taken by a given student (take student_id as input).
delimiter $$
create procedure student_all_courses(in SID int)
begin
	select c.course_name
    from enrollments e
    join students s on e.student_id = s.student_id
    join courses c on e.course_id = c.course_id
    where s.student_id = SID;
end$$
 
delimiter ;
call student_all_courses(1);


-- Create a stored procedure to show average grade per course.

DELIMITER $$
 
CREATE PROCEDURE GetAverageGrades()
BEGIN
SELECT c.course_name, CASE ROUND(AVG(CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            END))
            WHEN 4 THEN'A'
            WHEN 3 THEN'B'
            WHEN 2 THEN'C'
            WHEN 1 THEN'D'
            END AS AverageGrade
FROM Courses c
JOIN Enrollments e ON c.course_id=e.course_id
GROUP BY c.course_name;
END$$
 
DELIMITER ;
 
CALL GetAverageGrades();
 