use schooldb;

-- create employee table
create table employees(
	id int auto_increment primary key,
    name varchar(50) not null,
    age int, 
    department varchar(50),
    salary decimal 
);
	
-- inserting rows 
insert into employees (name, age, department, salary)
values ('raghav', 29, 'Software', 90000),
	('Vikas', 30, 'HR', 45000),
    ('Ravi', 25, 'IT', 50000),
    ('Umesh', 25, 'Accounts','55000');
    
-- selecting all

select * from employees ;
    
-- update 

update employees
SET salary = 47000
where id = 3 ;

update employees
SET department = 'HR'
where id = 4 ;

select * from employees;

delete from employees where id = '4';

