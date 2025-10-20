create database online_course_db;

use online_course_db;

CREATE TABLE courses (
    CourseID VARCHAR(10) PRIMARY KEY,
    Title VARCHAR(100),
    Category VARCHAR(50),
    Duration INT 
);

CREATE TABLE students (
    StudentID VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Country VARCHAR(50)
);


INSERT INTO courses (CourseID, Title, Category, Duration) VALUES
('C101', 'Python for Beginners', 'Programming', 40),
('C102', 'Machine Learning Basics', 'AI', 60),
('C103', 'Data Visualization with Power BI', 'Analytics', 30),
('C104', 'Cloud Fundamentals', 'Cloud', 50);


INSERT INTO students (StudentID, Name, Email, Country) VALUES
('S001', 'Neha', 'neha@abc.com', 'India'),
('S002', 'Arjun', 'arjun@abc.com', 'UAE'),
('S003', 'Rahul', 'rahul@abc.com', 'UK'),
('S004', 'Ravi', 'ravi@abc.com', 'India'),
('S005', 'Ron', 'ron@abc.com', 'USA');

-- 1. Add a New Course
INSERT INTO courses (CourseID, Title, Category, Duration)
VALUES ('C105', 'Advanced SQL', 'Database', 45);

-- 2. Update course duration
UPDATE courses
SET Duration = 70
WHERE CourseID = 'C102';

-- 3. delete a student 
DELETE FROM students
WHERE StudentID = 'S003';


-- 4. Fetch all the students from india 
SELECT * FROM students
WHERE Country = 'India';



