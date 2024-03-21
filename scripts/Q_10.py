import psycopg

with psycopg.connect("dbname=test user=postgres") as conn:

    with conn.cursor() as cur:

        # Q_10: In the La Liga season of 2020/2021, find the players that were least dribbled past. Sort them from lowest to highest.
           
        cur.execute("""
            insert query here
            """)