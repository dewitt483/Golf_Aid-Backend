import psycopg

conn_string = "postgresql://postgres:mysecretpassword@localhost:5432/mydb"

try:
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, email FROM users;")
            rows = cur.fetchall()
            print("Users:")
            for row in rows:
                print(row)
except Exception as e:
    print("Error querying data:", e)
