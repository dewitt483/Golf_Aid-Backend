# db.py
import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="mydb",  # or postgres if no DB was created
        user="postgres",
        password="mysecretpassword",
        host="localhost",
        port="5432"
    )
