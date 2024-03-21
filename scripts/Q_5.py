import psycopg

with psycopg.connect("dbname=test user=postgres") as conn:

    with conn.cursor() as cur:

        # Q_5: In the Premier League season of 2003/2004, find the players who were the most intended recipients of passes. Sort them from highest to lowest.

        cur.execute("""
            insert query here
            """)