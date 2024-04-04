# COMP3005-Project
Group members: Joey Villeneuve (101187383), Ben Seguin (101196580), Austin Rimmer (101219747)

This is a PostgreSQL project that uses Python and psycopg3 to create a database called "project_database" and query it.

How to install psycopg3:
- Open terminal.
- Run: pip install --upgrade pip
- Run: pip install "psycopg[binary]"

How to setup project_database: Run "project_database.py".
How to export project_database to .sql file: Execute 'pg_dump -U postgres -h localhost project_database >> dbexport.sql' in terminal.
How to run autograder: "queries.py" refers to the exported .sql file "dbexport.sql". Make sure it is correct, then run "queries.py".