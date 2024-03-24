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
data_directory = Path('C:/Users/joey/OneDrive/Documents/GitHub/data') # Where the StatsBomb data folder (use "/", not "\")

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
    CREATE TABLE competition (
        competition_id INT NOT NULL,
        country_name VARCHAR(30),
        competition_name VARCHAR(30),
        competition_gender VARCHAR(10),
        competition_youth BOOLEAN,
        competition_international BOOLEAN,
        PRIMARY KEY (competition_id)
    );
               
    CREATE TABLE season (
        competition_id INT NOT NULL,
        season_id INT NOT NULL,
        season_name VARCHAR(30),
        PRIMARY KEY (season_id),
        FOREIGN KEY (competition_id) REFERENCES competition(competition_id)
    );
               
    CREATE TABLE match (
        season_id INT NOT NULL,
        match_id INT NOT NULL,
        stadium_id INT NOT NULL,
        referee_id INT NOT NULL,
        match_date TIMESTAMP,
        match_week INT NOT NULL,
        kick_off TIMESTAMP,
        home_team_id INT NOT NULL,
        away_team_id INT NOT NULL,
        home_score INT NOT NULL,
        away_score INT NOT NULL,
        PRIMARY KEY (match_id),
        FOREIGN KEY (season_id) REFERENCES season(season_id)
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
            competitions_data = json.load(f)

        seen = []
        for competition in competitions_data:

            if (competition["competition_id"] not in seen):  # Insert each unique competition into competition table
                cursor.execute("INSERT INTO competition(competition_id, country_name, competition_name, competition_gender, competition_youth, competition_international) VALUES (%s, %s, %s, %s, %s, %s)",
                (competition["competition_id"], competition["country_name"], competition["competition_name"], competition["competition_gender"], competition["competition_youth"], competition["competition_international"]))
                seen.append(competition["competition_id"])

            # TO-DO: Find a way workaround for duplicate season_ids
            cursor.execute("INSERT INTO season(competition_id, season_id, season_name) VALUES (%s, %s, %s)", # Insert each target season into season table
            (competition["competition_id"], competition["season_id"], competition["season_name"]))
            

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
                            pass
                            #print(element["competition"]["competition_name"], element["season"])
            # Premier League
            elif (competition_id.name == "2"):
                for season_id in competition_id.iterdir():
                    if (season_id.name in target_seasons): # Only read season 2003/2004
                        with open(season_id, encoding="utf8") as f:
                            data = json.loads(f.read())
                        for element in data:
                            pass
                            #print(element["competition"]["competition_name"], element["season"])

# DEBUGGING ---------------------------------------- (delete before submitting)
cursor.execute('SELECT * FROM competition')
cursor.execute('SELECT * FROM season')
print(cursor.fetchall())

# CLOSE CONNECTION ---------------------------------
connection.commit()
cursor.close()
connection.close()
print("Script completed successfully.")