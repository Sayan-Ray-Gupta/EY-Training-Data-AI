-- Hospital Management System 
create database HospitalManagement ;
use HospitalManagement ;

 
Create table Patients (
	patient_id INT PRIMARY KEY,
	name VARCHAR(50),
	age INT,
	gender CHAR(1),
	city VARCHAR(50)
    );
    
create table Doctors (
	doctor_id INT PRIMARY KEY,
	name VARCHAR(50),
	specialization VARCHAR(50),
	experience INT
);

create table Appointments (
	appointment_id INT PRIMARY KEY,
	patient_id INT ,
	doctor_id INT ,
	appointment_date DATE,
	status VARCHAR(20),
    Foreign key (patient_id) references Patients(patient_id),
    foreign key (doctor_id) references Doctors(doctor_id)
    
);

create table MedicalRecords (
	record_id INT PRIMARY KEY,
	patient_id INT ,
	doctor_id INT ,
	diagnosis VARCHAR(100),
	treatment VARCHAR(100),
	date DATE,
    foreign key (patient_id) references Patients(patient_id),
    foreign key (doctor_id) references Doctors(doctor_id)
);


    
    
create table billings (

	bill_id INT PRIMARY KEY,
	patient_id INT,
	amount DECIMAL(10,2),
	bill_date DATE,
	status VARCHAR(20),
    foreign key (patient_id) references Patients(patient_id)
    
);


INSERT INTO Patients (patient_id, name, age, gender, city) VALUES
(101,'yash', 60, 'M', 'Hyderabad'),
(102,'vinay', 77, 'M', 'Mumbai'),
(103,'kaveri', 57, 'F', 'Kolkata'),
(104,'vikram', 37, 'M', 'Delhi'),
(105,'ashish', 29, 'M', 'Hyderabad'),
(106,'ritu', 55, 'F', 'Bengaluru'),
(107,'Manish', 80, 'M', 'Delhi'),
(108,'Rahul', 43, 'M', 'Mumbai'),
(109,'sonal', 32, 'F', 'Hyderabad,'),
(110,'disha', 48, 'M', 'Hyderabad');


-- Insert 5 Doctors (with various specializations)
INSERT INTO Doctors (doctor_id, name, specialization, experience) VALUES
(1, 'Dr. kush yadav', 'Cardiology', 10),
(2, 'Dr. Sumit Jana', 'Dermatology', 7),
(3, 'Dr. Arun Gupta', 'Neurology', 15),
(4, 'Dr. Shanlini Roy', 'ENT', 12),
(5, 'Dr. Varun Singh', 'Orthopedic', 6);


-- Insert Appointments
INSERT INTO Appointments (appointment_id, patient_id, doctor_id, appointment_date, status) VALUES
(1, 102, 1, '2025-10-30', 'Completed'),
(2, 104, 1, '2025-10-07', 'Scheduled'),
(3, 107, 3, '2025-10-08', 'Scheduled'),
(4, 109, 2, '2025-10-04', 'Scheduled'),
(5, 101, 4, '2025-10-04', 'Scheduled'),
(6, 108, 5, '2025-10-30', 'completed');
 
-- Insert Medical Records (linked to completed appointments)
INSERT INTO MedicalRecords (record_id, patient_id, doctor_id, diagnosis, treatment, date) VALUES
(2001, 102, 1, 'palpitation', 'Prescribe medication A', '2025-09-30'),
(2002, 108, 2, 'Fractured knee', 'Casting', '2025-09-30');
 
-- Insert Billing
INSERT INTO Billings (bill_id, patient_id, amount, bill_date, status) VALUES
(3001, 102, 500.00, '2025-09-29', 'Paid'),
(3002, 104, 850.50, '2025-10-01', 'Unpaid'), -- Unpaid Bill
(3003, 108, 6200.00, '2025-09-29', 'Paid'),
(3004, 101, 400.00, '2025-10-04', 'Unpaid'), -- Unpaid Bill
(3005, 108, 1200.00, '2025-10-03', 'paid'); 


-- Basic Queries
-- 1.List all patient assigned to cardiologist

Select distinct p.*
From patients p
Join Appointments a On p.patient_id = a.patient_id
Join Doctors d on a.doctor_id = d.doctor_id
where d.specialization = 'cardilogy';


-- 2. Find all appointment for a give doctor
select a.* , p.name as patient_name 
From appointments a 
join Patients p on a.patient_id = p.patient_id
where a.doctor_id = 2 ;

-- 3. show unpaid bills of patients 
Select b.* , p.name as patient_name
from billings b
join Patients p on b.patient_id = p.patient_id
where b.status = 'unpaid'



-- 4. 

delimiter $$
create procedure GetPatientHistory(IN in_patient_id INT)
begin
	select 
		mr.date,
        d.name as doctor_name,
        d.specialization,
        mr.diagnosis,
        mr.treatment
	from MedicalRecords mr 
    join doctors d on mr.doctor_id = d.doctor_id
    where mr.patient_id = in_patient_id
    order by mr.date desc;
end $$

delimiter ;
call GetPatientHistory(102)



-- 5 

Delimiter $$
create procedure GetDoctorAppointments(in in_doctor_id int)
Begin 
	select 
		a.appointment_id,
        a.appointment_date,
        a.status,
        p.name as patient_name,
        p.age,
        p.city
	from appointments a 
    join patients p on a.patient_id = p.patient_id
    where a.doctor_id = in_doctor_id
    Order by a.appointment_date Desc;
    
end $$
delimiter ;

Call GetDoctorAppointments(2)
