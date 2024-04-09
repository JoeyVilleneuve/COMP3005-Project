# COMP3005-Project
Group members: Joey Villeneuve (101187383), Ben Seguin (101196580), Austin Rimmer (101219747)

This is a PostgreSQL project that uses Python and psycopg3 to create a database called "project_database" and query it.

# Setup
1. Ensure that you have a PostgreSQL server running on your device with the user "postgres" and password "1234".
2. Install psycopg3:
  - Open terminal.
  - Run: pip install --upgrade pip
  - Run: pip install "psycopg[binary]"
3. In the "Code Submission" folder, unzip dbexport.zip (the .sql file is too large for GitHub's 100mb limit).
4. In project_database.py inside the "json_loader" folder, change the data_directory variable to be the filepath of the StatsBomb data folder on your device (the data folder exceed GitHub's upload limit).

How to setup project_database on your server: Run "project_database.py".
How to export project_database to .sql file: Execute 'pg_dump -U postgres -h localhost project_database >> dbexport.sql' in terminal (in Ubuntu environment for UTF-08 encoding).
How to run autograder: "queries.py" refers to the exported .sql file "dbexport.sql". Make sure it is correct, then run "queries.py".

# Team Contributions
Joey Villeneuve: Designed the database, made project_database.py script, made ER Model diagram, assisted with project report PDF.
Ben Seguin: Wrote queries 1-5, made Schema diagrams, wrote project report PDF.
Austin Rimmer: Wrote queries 6-10.
