import psycopg

with psycopg.connect("dbname=test user=postgres") as conn:

    with conn.cursor() as cur:

        # Q_3: In the La Liga seasons of 2020/2021, 2019/2020, and 2018/2019 combined, find the players with the most first-time shots. Sort them from highest to lowest.
        
        cur.execute("""
            insert query here
            """)