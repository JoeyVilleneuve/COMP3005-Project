import psycopg
import json
import sys
from pathlib import Path

# ESTABLISH CONNECTION -----------------------------
print("""
COMP3005 Group 9 Project - 'project_database' Script
Authors: Joey Villeneuve, Ben Seguin, Austin Rimmer
====================================================
TA - Please change login credentials as needed in-file before running.
      
""")

# TA: Change as needed
user = 'postgres'
password = 'green6'
host = 'localhost'
port = "5432"
data_directory = Path('C:/Users/gamer/OneDrive/Documents/GitHub/data') # Where the StatsBomb data folder (use "/", not "\")

# DROP then CREATE project_database (in case script was ran previously)
connection = psycopg.connect(dbname='postgres', user=user, password=password, host=host, port=port)
connection.autocommit = True
cursor = connection.cursor()
cursor.execute('DROP DATABASE IF EXISTS project_database')
cursor.execute('CREATE DATABASE project_database')

# Connect to project_database
connection = psycopg.connect(dbname='project_database', user=user, password=password, host=host, port=port)
connection.autocommit = True
cursor = connection.cursor()

# SET UP DATABASE ----------------------------------

# Create tables
cursor.execute("""
    CREATE TABLE competitions (
        competition_id INT NOT NULL,
        season_id INT NOT NULL,
        country_name VARCHAR(50),
        competition_name VARCHAR(50),
        competition_gender VARCHAR(50),
        competition_youth VARCHAR(50),
        competition_international VARCHAR(50),
        season_name VARCHAR(50) NOT NULL,
        match_updated TIMESTAMP,
        match_updated_360 TIMESTAMP,
        match_available_360 TIMESTAMP,
        match_available TIMESTAMP
    );
    """)

# Read in JSON files
target_seasons = ["4.json", "42.json", "90.json", "44.json"]
events_data = None
lineups_data = None
matches_data = None

for entry in data_directory.iterdir():

    if (entry.name == "competitions.json"): # Competitions
        with open(entry) as f:
            competitions_data = f.read()
        cursor.execute('INSERT INTO competitions SELECT * FROM json_populate_recordset(NULL::competitions, %s);', (competitions_data,))

    if (entry.name == "events"): # Events: Formatted as data/events/[match_id].json
        for file in entry.iterdir():
            pass

    if (entry.name == "lineups"): # Lineups: Formatted as data/lineups/[match_id].json
        for file in entry.iterdir():
            pass

    if (entry.name == "matches"): # Matches: Formatted as data/matches/[competition_id]/[season_id].json
        for competition_id in entry.iterdir():
            # La Liga
            if (competition_id.name == "11"):
                for season_id in competition_id.iterdir():
                    if (season_id.name in target_seasons): # Only read seasons 2018/2019, 2019/2020, 2020/2021
                        with open(season_id, encoding="utf8") as f:
                            data = json.loads(f.read())
                        for element in data:
                            print(element["competition"]["competition_name"], element["season"])
            # Premier League
            elif (competition_id.name == "2"):
                for season_id in competition_id.iterdir():
                    if (season_id.name in target_seasons): # Only read season 2003/2004
                        with open(season_id, encoding="utf8") as f:
                            data = json.loads(f.read())
                        for element in data:
                            print(element["competition"]["competition_name"], element["season"])

# DEBUGGING ---------------------------------------- (delete before submitting)
#cursor.execute('SELECT * FROM competitions')
#print(cursor.fetchall())

# CLOSE CONNECTION ---------------------------------
connection.commit()
cursor.close()
connection.close()
print("Script completed successfully.")