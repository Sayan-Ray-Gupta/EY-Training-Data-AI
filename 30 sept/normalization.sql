create database if not exists retailNF;
use retailNF;
 
create table badOrders(
	order_id int Primary key,
    order_date date,
    customer_id VARCHAR(200),
    customer_name VARCHAR(50),
    customer_city VARCHAR(50),
    product_id VARCHAR(200),
    product_name VARCHAR(200),
    unit_prices VARCHAR(200),
    quantities VARCHAR(200),
    order_total decimal(10,2)
);
INSERT INTO BadOrders VALUES
-- order_id, date, cust, name, city,     pids,      pnames, prices,        qtys,    total
(101, '2025-09-01', 1, 'Rahul', 'Mumbai', '1,3','Laptop,Headphones','60000,2000',  '1,2',   64000.00),
(102, '2025-09-02', 2, 'Priya', 'Delhi',  '2','Smartphone', '30000','1',     30000.00);


create table Orders_1nf (
	Order_id int primary key ,
    order_date date ,
    customer_id int,
    customer_name varchar(50) , 
    customer_city varchar(50)
);

create table OrderItems_1nf (
	order_id int,
    line_no int,
    product_id int,
    product_name varchar(50),
    unit_price decimal(10,2),
    quantity int, 
    primary key (order_id, line_no),
    foreign key (order_id) references Orders_1nf(Order_id)
);

-- load split rows (manually splitting the CSVs from BadOrders)
insert into Orders_1nf
Select order_id, order_date, customer_id, customer_name, customer_city
from BadOrders;


-- order 101 had 2 items -> 2 rows
insert into OrderItems_1nf values 
(101, 1, 1, 'laptop', 60000, 1),
(101, 2, 3, 'Headphone', 2000 , 2);

--  order 102 had 1 item -> 1 row
insert into OrderItems_1nf values
(102, 1, 2, 'Smartphone', 30000 , 1);


-- split customer now too ( prepping for 3nf )
create table Customers_2NF (
	customer_id int primary key ,
    customer_name varchar (50),
    customer_city varchar(50)
);

-- move orders to reference just customer_id 
create table Order_2NF (
	order_id int primary key ,
    order_date date,
    customer_id int, 
    foreign key (customer_id) references Customers_2NF(customer_id)
);

create table Products_2NF (
	product_id int primary key ,
    product_name varchar (50),
    category varchar(50),
    list_price decimal (10,2)
);

CREATE TABLE OrderItems_2NF (

  order_id INT,

  line_no INT,

  product_id INT,

  unit_price_at_sale DECIMAL(10,2),  -- historical price

  quantity INT,

  PRIMARY KEY (order_id, line_no),

  FOREIGN KEY (order_id) REFERENCES Order_2NF(order_id),

  FOREIGN KEY (product_id) REFERENCES Products_2NF(product_id)

);

-- Seed dimension tables (from what we saw in BadOrders/OrderItems_1NF)
INSERT INTO Customers_2NF VALUES
(1, 'Rahul', 'Mumbai'),
(2, 'Priya', 'Delhi');
 
INSERT INTO Products_2NF VALUES
(1, 'Laptop',     'Electronics', 60000),
(2, 'Smartphone', 'Electronics', 30000),
(3, 'Headphones', 'Accessories',  2000);
 
INSERT INTO Order_2NF VALUES
(101, '2025-09-01', 1),
(102, '2025-09-02', 2);
 
INSERT INTO OrderItems_2NF VALUES
(101, 1, 1, 60000, 1),
(101, 2, 3,  2000, 2),
(102, 1, 2, 30000, 1);
 
 
 
 
 -- 3nf 
 
 
 Create table cities (
	city_id int primary key, 
    city_name varchar (50),
	state varchar(50)
    
);

create table customers_3NF (
	customer_id INT PRIMARY KEY,
    customer_name varchar (50),
	city_id int ,
    foreign key (city_id) references cities(city_id)
);

-- Carry over ORDERS / Products / OrderItems to 3nf naming 

create table Products_3NF like Products_2NF;
insert into products_3NF select * From Products_2NF ; 

create table Order_3nf like Order_2nf;
create table OrderItems_3nf like OrderItems_2nf ;
    
    
-- seed cities + Customers (Mumbai -> maharastra, delhi -> Delhi)
insert into cities values 
(10, 'Mumbai',  'maharashtra'),
(20, 'Delhi', 'Delhi');

insert into customers_3nf values 
(1, 'rahul' , 10),
(2, 'priya' , 20);

insert into Order_3NF Select * From Order_2NF ;
insert into OrderItems_3NF Select * from OrderItems_2NF;
