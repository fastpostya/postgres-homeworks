import os

path_employees = os.sep.join(["homework-1", "north_data", "employees_data.csv"])
path_orders = os.sep.join(["homework-1", "north_data", "orders_data.csv"])
path_customers = os.sep.join(["homework-1",  "north_data", "customers_data.csv"])
path_sql = os.sep.join(["homework-1","create_tables.sql"])
password = os.getenv("PASSWORD_POSTGRESSQL")
database_name = "north"
