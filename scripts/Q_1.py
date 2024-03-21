import psycopg

with psycopg.connect("dbname=test user=postgres") as conn:

    with conn.cursor() as cur:

        # Q_1: In the La Liga season of 2020/2021, sort the players from highest to lowest based on their average xG scores.

        cur.execute("""
            insert query here
            """)