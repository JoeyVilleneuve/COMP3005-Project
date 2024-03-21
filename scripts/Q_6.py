import psycopg

with psycopg.connect("dbname=test user=postgres") as conn:

    with conn.cursor() as cur:

        # Q_6: In the Premier League season of 2003/2004, find the teams with the most shots made. Sort them from highest to lowest.   
          
        cur.execute("""
            insert query here
            """)