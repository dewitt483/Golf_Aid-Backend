import psycopg

conn_string = "postgresql://postgres:mysecretpassword@localhost:5432/mydb"

try:
    with psycopg.connect(conn_string) as conn:
        with conn.cursor() as cur:
            # Create table
            cur.execute("""
               CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL
                );
            """)
            conn.commit()
            cur.execute("""
               CREATE TABLE IF NOT EXISTS rounds (
                    rid serial PRIMARY KEY,
                    username TEXT NOT NULL,
                    score integer NOT NULL, 
                    FOREIGN KEY (username) REFERENCES users(username)
                );
            """)
            conn.commit()
            print("Table created successfully.")
except Exception as e:
    print("Error creating table:", e)

