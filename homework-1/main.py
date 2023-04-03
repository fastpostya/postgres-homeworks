import csv
import os
import psycopg2
from config import password, path_customers, path_employees, path_orders
from config import database_name, path_sql


def main():
    """Скрипт для заполнения данными таблиц в БД Postgres."""

    drop_all(password, database_name)
    text = create_employees(password, database_name, path_employees)
    print_table(password, database_name, 'employees_data')

    text += create_customer_data(password, database_name, path_customers)
    print_table(password, database_name, 'customers_data')

    text += create_orders_data(password, database_name, path_orders)
    print_table(password, database_name, 'orders_data')

    with open(path_sql, "w", encoding="utf-8") as file:
        file.write(text)


def drop_all(password, database_name):
    with psycopg2.connect(
        host="localhost",
        database=database_name,
        user="postgres",
        password=password
    ) as conn:
        with conn.cursor() as cur:
            drop_text = '''
            DROP TABLE orders_data;
            DROP TABLE employees_data;
            DROP TABLE customers_data;
            '''
            cur.execute(drop_text)


def change_apostrophe(text: str) -> str:
    return text.replace("'", "''")


def create_customer_data(password, database_name, path) -> str:
    # "customer_id","company_name","contact_name"
    text_query = ""
    with psycopg2.connect(
        host="localhost",
        database=database_name,
        user="postgres",
        password=password
    ) as conn:
        with conn.cursor() as cur:
            create_text = '''CREATE TABLE customers_data(
                customer_id varchar(50) PRIMARY KEY NOT NULL,
                company_name varchar(100) NOT NULL,
                contact_name varchar(100) NOT NULL
                )'''
            text_query += create_text + "\n"
            cur.execute(create_text)
            if os.path.exists(path) and os.path.isfile(path):
                with open(path, "r", newline='', encoding='utf-8') as csvfile:
                    csv_data = csv.DictReader(csvfile)
                    # "customer_id","company_name","contact_name"
                    if not (("customer_id" in csv_data.fieldnames)\
                        and ("company_name" in csv_data.fieldnames)\
                        and ("contact_name"  in csv_data.fieldnames)):
                        # raise InstantiateCSVError(f"Файл {path} поврежден")
                        print(f"Файл {path} поврежден")
                    else:
                        current = 1
                        for row in csv_data:
                            customer_id = row["customer_id"]
                            company_name = change_apostrophe(row["company_name"])
                            contact_name = row["contact_name"]
                            insert_text = 'INSERT INTO customers_data VALUES'
                            insert_text += f"('{customer_id}', "
                            insert_text += f"'{company_name}', '{contact_name}');"
                            # text_query += insert_text + "\n"
                            cur.execute(insert_text)
                            current += 1
                        conn.commit()
                        return text_query
            else:
                raise FileNotFoundError(f"Отсутствует файл {path}")


def create_orders_data(password, database_name, path) -> str:
    # "order_id","customer_id","employee_id","order_date","ship_city"
    text_query = ""
    with psycopg2.connect(
        host="localhost",
        database=database_name,
        user="postgres",
        password=password
    ) as conn:
        with conn.cursor() as cur:
            create_text = '''CREATE TABLE orders_data(
                order_id int PRIMARY KEY NOT NULL,
                customer_id varchar(50) REFERENCES customers_data(customer_id) NOT NULL,
                employee_id int REFERENCES employees_data(employee_id) NOT NULL,
                order_date date NOT NULL,
                ship_city varchar(50) NOT NULL
                )'''
            text_query += create_text + "\n"
            cur.execute(create_text)
            if os.path.exists(path) and os.path.isfile(path):
                with open(path, "r", newline='', encoding='utf-8') as csvfile:
                    csv_data = csv.DictReader(csvfile)
                    # "order_id","customer_id","employee_id","order_date","ship_city"
                    if not (("order_id" in csv_data.fieldnames)\
                        and ("customer_id" in csv_data.fieldnames)\
                        and ("employee_id" in csv_data.fieldnames)\
                        and ("order_date"  in csv_data.fieldnames)\
                        and ("ship_city"  in csv_data.fieldnames)):
                        # raise InstantiateCSVError(f"Файл {path} поврежден")
                        print(f"Файл {path} поврежден")
                    else:
                        current = 1
                        for row in csv_data:
                            order_id = row["order_id"]
                            customer_id = row["customer_id"]
                            employee_id = row["employee_id"]
                            order_date = row["order_date"]
                            ship_city = row["ship_city"]
                            insert_text = 'INSERT INTO orders_data VALUES'
                            insert_text += f"({order_id}, '{customer_id}', "
                            # DATE '2021-10-01', DATE и дата в формате 'yyyy-mm-dd'
                            insert_text += f"{employee_id}, DATE '{order_date}', '{ship_city}');"
                            # text_query += insert_text + "\n"
                            cur.execute(insert_text)
                            current += 1
                        conn.commit()
                        return text_query
            else:
                raise FileNotFoundError(f"Отсутствует файл {path}")


def create_employees(password, database_name, path) -> str:
    text_query = ""
    with psycopg2.connect(
        host="localhost",
        database=database_name,
        user="postgres",
        password=password
    ) as conn:
        with conn.cursor() as cur:
            create_text = '''CREATE TABLE employees_data(
                employee_id int PRIMARY KEY,
                first_name varchar(50) NOT NULL,
                last_name varchar(50) NOT NULL,
                title varchar(100),
                birth_date date,
                notes varchar(600)
                )'''
            text_query += create_text + "\n"
            cur.execute(create_text)
            if os.path.exists(path) and os.path.isfile(path):
                with open(path, "r", newline='', encoding='utf-8') as csvfile:
                    csv_data = csv.DictReader(csvfile)
                    if not (("first_name" in csv_data.fieldnames)\
                        and ("last_name" in csv_data.fieldnames)\
                        and ("title" in csv_data.fieldnames)\
                        and ("birth_date"  in csv_data.fieldnames)\
                        and ("notes"  in csv_data.fieldnames)):
                        # raise InstantiateCSVError(f"Файл {path} поврежден")
                        print(f"Файл {path} поврежден")
                    else:
                        current = 1
                        for row in csv_data:
                            first_name = row["first_name"]
                            last_name = row["last_name"]
                            title = row["title"]
                            birth_date = row["birth_date"]
                            notes = row["notes"]
                            insert_text = 'INSERT INTO employees_data VALUES'
                            insert_text += f"({current}, '{first_name}', '{last_name}', "
                            # DATE '2021-10-01', DATE и дата в формате 'yyyy-mm-dd'
                            insert_text += f"'{title}', DATE '{birth_date}', '{notes}');"
                            # text_query += insert_text + "\n"
                            cur.execute(insert_text)
                            current += 1
                        conn.commit()
                        return text_query
            else:
                raise FileNotFoundError(f"Отсутствует файл {path}")


def print_table(password, database_name, table_name):
    with psycopg2.connect(
        host="localhost",
        database=database_name,
        user="postgres",
        password=password
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table_name}")
            rows = cur.fetchall()
            for row in rows:
                print(row)


if __name__ == "__main__":
    main()
    # path = path_employees
    # print(f'os.path.exists({path})=', os.path.exists(path))
    # print(os.listdir())
