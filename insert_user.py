import psycopg

conn_string = "postgresql://postgres:mysecretpassword@localhost:5432/mydb"

try:
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            # Insert a user
            cur.execute("""
                INSERT INTO users (name, email)
                VALUES (%s, %s)
                RETURNING id;
            """, ("Alice", "alice@example.com"))
            user_id = cur.fetchone()[0]
            conn.commit()
            print(f"Inserted user with ID {user_id}")
except Exception as e:
    print("Error inserting data:", e)
