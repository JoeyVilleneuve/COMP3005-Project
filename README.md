# COMP3005-Project
Group members: Joey Villeneuve (101187383), Ben Seguin (101196580), Austin Rimmer (101219747)

This is a Python PostgreSQL project that uses psycopg3.

How to install psycopg3:
- Open terminal.
- Run: pip install --upgrade pip
- Run: pip install "psycopg[binary]"

# How-To Guide: Psycopg in Python
    import psycopg
   
    with psycopg.connect("dbname=test user=postgres") as conn:
    
        # How to open a cursor to perform database operations
        with conn.cursor() as cur:
    
            # How to execute a command
            cur.execute("""
                CREATE TABLE test (
                    id serial PRIMARY KEY,
                    num integer,
                    data text)
                """)
    
            # How to pass data into a command
            cur.execute(
                "INSERT INTO test (num, data) VALUES (%s, %s)",
                (100, "abc'def"))
    
            # How to retrieve data from a query
            cur.execute("SELECT * FROM test")
            cur.fetchone() # Returns (1, 100, "abc'def"). Alternatively, can use "cur.fetchmany()", "cur.fetchall()" to return a list of several records
            
            # How to iterate the cursor
            for record in cur:
                print(record)
    
            # How to make the changes to the database persistent
            conn.commit()
