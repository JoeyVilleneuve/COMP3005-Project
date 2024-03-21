import psycopg

with psycopg.connect("dbname=test user=postgres") as conn:

    with conn.cursor() as cur:

        # Q_4: In the La Liga season of 2020/2021, find the teams with the most passes made. Sort them from highest to lowest.        
        
        cur.execute("""
            insert query here
            """)