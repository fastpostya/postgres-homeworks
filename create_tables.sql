CREATE TABLE employees_data(
                employee_id int PRIMARY KEY,
                first_name varchar(50) NOT NULL,
                last_name varchar(50) NOT NULL,
                title varchar(100),
                birth_date date,
                notes varchar(600)
                )
CREATE TABLE customers_data(
                customer_id varchar(50) PRIMARY KEY NOT NULL,
                company_name varchar(100) NOT NULL,
                contact_name varchar(100) NOT NULL
                )
CREATE TABLE orders_data(
                order_id int PRIMARY KEY NOT NULL,
                customer_id varchar(50) REFERENCES customers_data(customer_id) NOT NULL,
                employee_id int REFERENCES employees_data(employee_id) NOT NULL,
                order_date date NOT NULL,
                ship_city varchar(50) NOT NULL
                )
