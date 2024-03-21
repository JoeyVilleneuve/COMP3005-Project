import psycopg

with psycopg.connect("dbname=test user=postgres") as conn:

    with conn.cursor() as cur:

        # Q_7: In the La Liga season of 2020/2021, find the players who made the most through balls. Sort them from highest to lowest.

        cur.execute("""
            insert query here
            """)