import psycopg
import json
from pathlib import Path

# ESTABLISH CONNECTION -----------------------------
print("""
COMP3005 Group 9 Project - 'project_database' Script
Authors: Joey Villeneuve, Ben Seguin, Austin Rimmer
====================================================
TA - Please change login credentials as needed in-file before running.
      
Creating database, this may take a minute...
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
        competition_country VARCHAR(30),
        competition_name VARCHAR(30),
        competition_gender VARCHAR(10),
        competition_youth BOOLEAN,
        competition_international BOOLEAN,
        PRIMARY KEY (competition_id)
    );
               
    CREATE TABLE season (
        season_id INT NOT NULL,
        competition_id INT NOT NULL,
        season_name VARCHAR(30),
        PRIMARY KEY (season_id),
        FOREIGN KEY (competition_id) REFERENCES competition(competition_id)
    );
               
    CREATE TABLE match (
        match_id INT NOT NULL,
        season_id INT NOT NULL,
        stadium_id INT,
        referee_id INT,
        match_date TIMESTAMP,
        match_week INT NOT NULL,
        kick_off TIME,
        home_team_id INT NOT NULL,
        away_team_id INT NOT NULL,
        home_score INT,
        away_score INT,
        home_lineup_id INT,
        away_lineup_id INT,
        PRIMARY KEY (match_id),
        FOREIGN KEY (season_id) REFERENCES season(season_id)
    );
               
    CREATE TABLE manager (
        manager_id INT NOT NULL,
        manager_name VARCHAR(40),
        manager_nickname VARCHAR(30),
        manager_dob TIMESTAMP,
        manager_country VARCHAR(20),
        PRIMARY KEY (manager_id)      
    );
               
    CREATE TABLE team (
        team_id INT NOT NULL,
        team_name VARCHAR(30),
        team_gender VARCHAR(10),
        team_country VARCHAR(20),
        manager_id INT,
        PRIMARY KEY (team_id),
        FOREIGN KEY (manager_id) REFERENCES manager(manager_id)
    );
               
    CREATE TABLE stadium (
        stadium_id INT NOT NULL,
        stadium_name VARCHAR(40),
        stadium_country VARCHAR(20),
        PRIMARY KEY (stadium_id)         
    );
               
    CREATE TABLE referee (
        referee_id INT NOT NULL,
        referee_name VARCHAR(50),
        referee_country VARCHAR(30),
        PRIMARY KEY (referee_id)
    );
               
    CREATE TABLE player (
        player_id INT NOT NULL,
        player_name VARCHAR(50),
        player_nickname VARCHAR(30),
        player_number INT NOT NULL,
        player_country VARCHAR(40),
        PRIMARY KEY (player_id)
    );
            
    CREATE TABLE lineup (
        lineup_id SERIAL,
        PRIMARY KEY (lineup_id)
    );
               
    CREATE TABLE position (
        position_id SERIAL,
        lineup_id INT NOT NULL,
        player_id INT NOT NULL,
        position_name VARCHAR(30),
        position_from VARCHAR(5),
        position_to VARCHAR(5),
        from_period INT,
        to_period INT,
        start_reason VARCHAR(50),
        end_reason VARCHAR(50),
        PRIMARY KEY (position_id),
        FOREIGN KEY (lineup_id) REFERENCES lineup(lineup_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)
    );
               
    CREATE TABLE card (
        card_id SERIAL,
        lineup_id INT NOT NULL,
        player_id INT NOT NULL,
        card_type VARCHAR(20),
        card_time VARCHAR(5), 
        card_reason VARCHAR(30),
        card_period INT,
        PRIMARY KEY (card_id),
        FOREIGN KEY (lineup_id) REFERENCES lineup(lineup_id)
    );

    CREATE TABLE event (
        event_id VARCHAR(40) NOT NULL,
        match_id INT NOT NULL,  
        event_index INT,
        event_period INT NOT NULL,
        event_timestamp VARCHAR(15),
        possession_index INT,
        possession_team_id INT NOT NULL,
        team_id INT NOT NULL,   
        play_pattern VARCHAR(30),          
        PRIMARY KEY (event_id),
        FOREIGN KEY (match_id) REFERENCES match(match_id)
    );
               
    CREATE TABLE ball_recovery (
        ball_recovery_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        recovery_failure BOOLEAN DEFAULT 'false',
        PRIMARY KEY (ball_recovery_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)         
    );
               
    CREATE TABLE dispossessed (
        dispossessed_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        PRIMARY KEY (dispossessed_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id) 
    );
               
    CREATE TABLE duel (
        duel_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        counterpress BOOLEAN DEFAULT 'false',
        type VARCHAR(20),
        outcome VARCHAR(20),
        PRIMARY KEY (duel_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)
    );

    CREATE TABLE camera_on (
        camera_on_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        PRIMARY KEY (camera_on_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id) 
    );
               
    CREATE TABLE block (
        block_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        PRIMARY KEY (block_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id) 
    );

    CREATE TABLE offside (
        offside_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        PRIMARY KEY (offside_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id) 
    );
               
    CREATE TABLE clearance (
        clearance_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        PRIMARY KEY (clearance_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id) 
    );
               
    CREATE TABLE interception (
        interception_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        outcome VARCHAR(20),
        PRIMARY KEY (interception_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id) 
    );
               
    CREATE TABLE dribble (
        dribble_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        outcome VARCHAR(20),
        PRIMARY KEY (dribble_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)
    );

    CREATE TABLE pass (
        pass_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        end_location VARCHAR(20),
        duration INT,
        recipient_id INT,
        length INT,
        angle INT,
        height VARCHAR(20),
        body_part VARCHAR(20),
        type VARCHAR(20),
        PRIMARY KEY (pass_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id),
        FOREIGN KEY (recipient_id) REFERENCES player(player_id)
    );

    CREATE TABLE shot (
        shot_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        end_location VARCHAR(20),
        duration INT,
        xg INT,
        key_pass_id VARCHAR(40),
        outcome VARCHAR(20),
        body_part VARCHAR(20),
        technique VARCHAR(20),
        type VARCHAR(20),
        PRIMARY KEY (shot_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id),
        FOREIGN KEY (key_pass_id) REFERENCES event(event_id)
    );

    CREATE TABLE ball_receipt (
        ball_receipt_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        PRIMARY KEY (ball_receipt_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)
    );
               
    """)

# Read in JSON files
target_competitions = [11,2] # La Liga / Premier League
target_seasons = [4,42,90,44] # La Liga seasons 2018/2019, 2019/2020, 2020/2021 / Premier League season 2003/2004 
seen_matches = []

for entry in data_directory.iterdir(): # Read in competitions & matches first

    if (entry.name == "competitions.json"): # Competitions: Formatted as a single .json file.
        seen_competitions = []
        with open(entry) as f:
            competitions_data = json.load(f)
        for competition in competitions_data:

            # Insert each unique competition into competition table
            if (competition["competition_id"] not in seen_competitions):
                cursor.execute("INSERT INTO competition(competition_id, competition_country, competition_name, competition_gender, competition_youth, competition_international) VALUES (%s, %s, %s, %s, %s, %s)",
                (competition["competition_id"], competition["country_name"], competition["competition_name"], competition["competition_gender"], competition["competition_youth"], competition["competition_international"]))
                seen_competitions.append(competition["competition_id"])

            # Insert each target season from each target competition into season table
            if (competition["competition_id"] in target_competitions and competition["season_id"] in target_seasons):
                cursor.execute("INSERT INTO season(season_id, competition_id, season_name) VALUES (%s, %s, %s)",
                (competition["season_id"], competition["competition_id"], competition["season_name"]))             

    elif (entry.name == "matches"): # Matches: Formatted as data/matches/[competition_id]/[season_id].json
        seen_managers = []
        seen_teams = []
        seen_stadiums = []
        seen_referees = []
        for competition in entry.iterdir():
            if (int(competition.name) in target_competitions):
                for season in competition.iterdir():
                    if (int((season.name).split(".")[0]) in target_seasons): # Remove '.json' from filename
                        with open(season, encoding="utf8") as f:
                            data = json.loads(f.read())
                        for match in data: 

                            # Insert each match into match table
                            cursor.execute("INSERT INTO match(match_id, season_id, match_date, match_week, kick_off, home_team_id, away_team_id, home_score, away_score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (match["match_id"], match["season"]["season_id"], match["match_date"], match["match_week"], match["kick_off"], match["home_team"]["home_team_id"], match["away_team"]["away_team_id"], match["home_score"], match["away_score"]))
                            if ("referee" in match): # Insert referee data if it exists
                                cursor.execute("UPDATE match SET referee_id = %s WHERE match_id = %s", (match["referee"]["id"], match["match_id"]))
                            if ("stadium" in match): # Insert stadium data if it exists
                                cursor.execute("UPDATE match SET stadium_id = %s WHERE match_id = %s", (match["stadium"]["id"], match["match_id"]))
                            seen_matches.append(match["match_id"])
                            
                            # Insert each unique manager into manager table if it exists
                            if ("managers" in match["home_team"]): # Home team
                                if (match["home_team"]["managers"][0]["id"] not in seen_managers):
                                    cursor.execute("INSERT INTO manager(manager_id, manager_name, manager_nickname, manager_dob, manager_country) VALUES (%s, %s, %s, %s, %s)",
                                    (match["home_team"]["managers"][0]["id"], match["home_team"]["managers"][0]["name"], match["home_team"]["managers"][0]["nickname"], match["home_team"]["managers"][0]["dob"], match["home_team"]["managers"][0]["country"]["name"]))
                                    seen_managers.append(match["home_team"]["managers"][0]["id"])
                            if ("managers" in match["away_team"]): # Away team
                                if (match["away_team"]["managers"][0]["id"] not in seen_managers):
                                    cursor.execute("INSERT INTO manager(manager_id, manager_name, manager_nickname, manager_dob, manager_country) VALUES (%s, %s, %s, %s, %s)",
                                    (match["away_team"]["managers"][0]["id"], match["away_team"]["managers"][0]["name"], match["away_team"]["managers"][0]["nickname"], match["away_team"]["managers"][0]["dob"], match["away_team"]["managers"][0]["country"]["name"]))
                                    seen_managers.append(match["away_team"]["managers"][0]["id"])

                            # Insert each unique team into team table
                            if (match["home_team"]["home_team_id"] not in seen_teams): # Home team
                                cursor.execute("INSERT INTO team(team_id, team_name, team_gender, team_country) VALUES (%s, %s, %s, %s)",
                                (match["home_team"]["home_team_id"], match["home_team"]["home_team_name"], match["home_team"]["home_team_gender"], match["home_team"]["country"]["name"]))
                                if ("managers" in match["home_team"]): # Insert manager data if it exists
                                    cursor.execute("UPDATE team SET manager_id = %s WHERE team_id = %s", (match["home_team"]["managers"][0]["id"], match["home_team"]["home_team_id"]))
                                seen_teams.append(match["home_team"]["home_team_id"])
                            if (match["away_team"]["away_team_id"] not in seen_teams): # Away team
                                cursor.execute("INSERT INTO team(team_id, team_name, team_gender, team_country) VALUES (%s, %s, %s, %s)",
                                (match["away_team"]["away_team_id"], match["away_team"]["away_team_name"], match["away_team"]["away_team_gender"], match["away_team"]["country"]["name"]))
                                if ("managers" in match["away_team"]): # Insert manager data if it exists
                                    cursor.execute("UPDATE team SET manager_id = %s WHERE team_id = %s", (match["away_team"]["managers"][0]["id"], match["away_team"]["away_team_id"]))
                                seen_teams.append(match["away_team"]["away_team_id"])

                            # Insert each unique stadium into stadium table if it exists
                            if ("stadium" in match):
                                if (match["stadium"]["id"] not in seen_stadiums):
                                    cursor.execute("INSERT INTO stadium(stadium_id, stadium_name, stadium_country) VALUES (%s, %s, %s)",
                                    (match["stadium"]["id"], match["stadium"]["name"], match["stadium"]["country"]["name"]))
                                    seen_stadiums.append(match["stadium"]["id"])

                            # Insert each unique referee into referee table if it exists
                            if ("referee" in match):
                                if (match["referee"]["id"] not in seen_referees):
                                    cursor.execute("INSERT INTO referee(referee_id, referee_name, referee_country) VALUES (%s, %s, %s)",
                                    (match["referee"]["id"], match["referee"]["name"], match["referee"]["country"]["name"]))
                                    seen_referees.append(match["referee"]["id"])
        connection.commit()

for entry in data_directory.iterdir(): # Read in lineups after seen_matches has been filled (we only care about data related to those matches)
    
    if (entry.name == "lineups"): # Lineups: Formatted as data/lineups/[match_id].json
        seen_players = []
        num_lineups = 0
        for m in entry.iterdir():
            match_number = int((m.name).split(".")[0])
            if (match_number in seen_matches): # Remove '.json' from filename
                with open(m, encoding="utf8") as f:
                    data = json.loads(f.read())
                for lineup in data:
                    
                    # Create a new lineup entry for each lineup
                    cursor.execute("INSERT INTO lineup DEFAULT VALUES")
                    num_lineups+=1
                    # Connect lineups to corresponding match, 2 lineups per match (uneven num_lineups = home team, even num_lineups = away team)
                    if(num_lineups % 2 == 0):
                        cursor.execute("UPDATE match SET away_lineup_id = %s WHERE match_id = %s", (num_lineups, match_number))
                    else:
                        cursor.execute("UPDATE match SET home_lineup_id = %s WHERE match_id = %s", (num_lineups, match_number))
                    
                    for element in lineup["lineup"]:

                        # Insert each unique player into player table
                        if (element["player_id"] not in seen_players):
                            cursor.execute("INSERT INTO player(player_id, player_name, player_nickname, player_number, player_country) VALUES (%s, %s, %s, %s, %s)",
                            (element["player_id"], element["player_name"], element["player_nickname"], element["jersey_number"], element["country"]["name"]))
                            seen_players.append(element["player_id"])

                        # Create a new position entry for each position
                        for position in element["positions"]:
                            cursor.execute("INSERT INTO position(lineup_id, player_id, position_name, position_from, position_to, from_period, to_period, start_reason, end_reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (num_lineups, element["player_id"], position["position"], position["from"], position["to"], position["from_period"], position["to_period"], position["start_reason"], position["end_reason"]))

                        # Create a new card entry for each card
                        for card in element["cards"]:
                            cursor.execute("INSERT INTO card(lineup_id, player_id, card_type, card_time, card_reason, card_period) VALUES (%s, %s, %s, %s, %s, %s)",
                            (num_lineups, element["player_id"], card["card_type"], card["time"], card["reason"], card["period"]))
        connection.commit()

for entry in data_directory.iterdir(): # Read in events after lineups have been filled (we need all players to exist)

    if (entry.name == "events"): # Events: Formatted as data/events/[match_id].json

        for m in entry.iterdir():
            match_number = int((m.name).split(".")[0])
            if (match_number in seen_matches): # Remove '.json' from filename
                with open(m, encoding="utf8") as f:
                    data = json.loads(f.read())

                args = "" # There are hundreds of thousands of events, grouping many INSERTs into less cursor commands is far faster

                for event in data: # We want each event to be a single INSERT rather than using UPDATEs, code cleanliness will suffer...

                    # Insert each event into event table
                    args += "INSERT INTO event(event_id, match_id, event_index, event_period, event_timestamp, possession_index, possession_team_id, team_id, play_pattern) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(event["id"], match_number, event["index"], event["period"], event["timestamp"], event["possession"], event["possession_team"]["id"], event["team"]["id"], event["play_pattern"]["name"])

                    # Each event type has its own table which link to the related event_id
                    event_type = event["type"]["id"]
                    match event_type:

                        case 2: # Ball recovery
                            if ("ball_recovery" in event and "recovery_failure" in event["ball_recovery"]):
                                args += "INSERT INTO ball_recovery(event_id, player_id, location, recovery_failure) VALUES ('{}', '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["ball_recovery"]["recovery_failure"])
                            else:
                                args += "INSERT INTO ball_recovery(event_id, player_id, location) VALUES ('{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"])

                        case 3: # Dispossessed
                            args += "INSERT INTO dispossessed(event_id, player_id, location) VALUES ('{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"])

                        case 4: # Duel
                            if ("counterpress" in event and "outcome" in event):
                                args += "INSERT INTO duel(event_id, player_id, location, type, counterpress, outcome) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["duel"]["type"]["name"], event["counterpress"], event["duel"]["outcome"]["name"])
                            elif ("counterpress" in event):
                                args += "INSERT INTO duel(event_id, player_id, location, type, counterpress) VALUES ('{}', '{}', '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["duel"]["type"]["name"], event["counterpress"])
                            elif ("outcome" in event["duel"]):
                                args += "INSERT INTO duel(event_id, player_id, location, type, outcome) VALUES ('{}', '{}', '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["duel"]["type"]["name"], event["duel"]["outcome"]["name"])
                            else:
                                args += "INSERT INTO duel(event_id, player_id, location, type) VALUES ('{}', '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["duel"]["type"]["name"])

                        case 5: # Camera On
                            args += "INSERT INTO camera_on(event_id, player_id) VALUES ('{}', '{}');".format(event["id"], event["player"]["id"])

                        case 6: # Block
                            args += "INSERT INTO block(event_id, player_id, location) VALUES ('{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"])

                        case 8: # Offside
                            args += "INSERT INTO offside(event_id, player_id, location) VALUES ('{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"])

                        case 9: # Clearance
                            args += "INSERT INTO clearance(event_id, player_id, location) VALUES ('{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"])

                        case 10: # Interception
                            args += "INSERT INTO interception(event_id, player_id, location, outcome) VALUES ('{}', '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["interception"]["outcome"]["name"])

                        case 14: # Dribble
                            args += "INSERT INTO dribble(event_id, player_id, location, outcome) VALUES ('{}', '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["dribble"]["outcome"]["name"])

                        case 16: # Shot
                            if ("key_pass_id" in event["shot"]):
                                args += "INSERT INTO shot(event_id, player_id, location, end_location, duration, xg, outcome, body_part, technique, type, key_pass_id) VALUES ('{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["shot"]["end_location"], event["duration"], event["shot"]["statsbomb_xg"], event["shot"]["outcome"]["name"], event["shot"]["body_part"]["name"], event["shot"]["technique"]["name"], event["shot"]["type"]["name"], event["shot"]["key_pass_id"])
                            else:
                                args += "INSERT INTO shot(event_id, player_id, location, end_location, duration, xg, outcome, body_part, technique, type) VALUES ('{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["shot"]["end_location"], event["duration"], event["shot"]["statsbomb_xg"], event["shot"]["outcome"]["name"], event["shot"]["body_part"]["name"], event["shot"]["technique"]["name"], event["shot"]["type"]["name"])
                        
                        case 17: # Pressure
                            pass
                        
                        case 18: # Half start
                            pass
                        
                        case 19: # Substitution
                            pass
                        
                        case 20: # Own goal against
                            pass
                        
                        case 21: # Foul won
                            pass
                        
                        case 22: # Foul committed
                            pass
                        
                        case 23: # Goal keeper
                            pass
                        
                        case 24: # Bad behaviour
                            pass
                        
                        case 25: # Own goal for
                            pass
                        
                        case 26: # Player on
                            pass
                        
                        case 27: # Player off
                            pass
                        
                        case 28: # Shield
                            pass
                        
                        case 30: # Pass     
                            event_pass = event["pass"] # Frustratingly, passes have 3 fields of data that *maybe* exist, have to account for all combinations to use only one INSERT
                            if ("recipient" in event_pass and "body_part" in event_pass and "type" in event_pass):
                                args += "INSERT INTO pass(event_id, player_id, location, end_location, duration, length, angle, height, recipient_id, body_part, type) VALUES ('{}', '{}', '{}', '{}', {}, {}, {}, '{}', '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["pass"]["end_location"], event["duration"], event["pass"]["length"], event["pass"]["angle"], event["pass"]["height"]["name"], event["pass"]["recipient"]["id"], event["pass"]["body_part"]["name"], event["pass"]["type"]["name"])
                            elif ("recipient" in event_pass and "body_part" in event_pass):
                                args += "INSERT INTO pass(event_id, player_id, location, end_location, duration, length, angle, height, recipient_id, body_part) VALUES ('{}', '{}', '{}', '{}', {}, {}, {}, '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["pass"]["end_location"], event["duration"], event["pass"]["length"], event["pass"]["angle"], event["pass"]["height"]["name"], event["pass"]["recipient"]["id"], event["pass"]["body_part"]["name"])
                            elif ("recipient" in event_pass and "type" in event_pass):
                                args += "INSERT INTO pass(event_id, player_id, location, end_location, duration, length, angle, height, recipient_id, type) VALUES ('{}', '{}', '{}', '{}', {}, {}, {}, '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["pass"]["end_location"], event["duration"], event["pass"]["length"], event["pass"]["angle"], event["pass"]["height"]["name"], event["pass"]["recipient"]["id"], event["pass"]["type"]["name"])
                            elif ("recipient" in event_pass):
                                args += "INSERT INTO pass(event_id, player_id, location, end_location, duration, length, angle, height, recipient_id) VALUES ('{}', '{}', '{}', '{}', {}, {}, {}, '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["pass"]["end_location"], event["duration"], event["pass"]["length"], event["pass"]["angle"], event["pass"]["height"]["name"], event["pass"]["recipient"]["id"])
                            elif ("body_part" in event_pass and "type" in event_pass):
                                args += "INSERT INTO pass(event_id, player_id, location, end_location, duration, length, angle, height, body_part, type) VALUES ('{}', '{}', '{}', '{}', {}, {}, {}, '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["pass"]["end_location"], event["duration"], event["pass"]["length"], event["pass"]["angle"], event["pass"]["height"]["name"], event["pass"]["body_part"]["name"], event["pass"]["type"]["name"])
                            elif ("body_part" in event_pass):
                                args += "INSERT INTO pass(event_id, player_id, location, end_location, duration, length, angle, height, body_part) VALUES ('{}', '{}', '{}', '{}', {}, {}, {}, '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["pass"]["end_location"], event["duration"], event["pass"]["length"], event["pass"]["angle"], event["pass"]["height"]["name"], event["pass"]["body_part"]["name"])
                            elif ("type" in event_pass):
                                args += "INSERT INTO pass(event_id, player_id, location, end_location, duration, length, angle, height, type) VALUES ('{}', '{}', '{}', '{}', {}, {}, {}, '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["pass"]["end_location"], event["duration"], event["pass"]["length"], event["pass"]["angle"], event["pass"]["height"]["name"], event["pass"]["type"]["name"])
                            else:
                                args += "INSERT INTO pass(event_id, player_id, location, end_location, duration, length, angle, height) VALUES ('{}', '{}', '{}', '{}', {}, {}, {}, '{}');".format(event["id"], event["player"]["id"], event["location"], event["pass"]["end_location"], event["duration"], event["pass"]["length"], event["pass"]["angle"], event["pass"]["height"]["name"])
                        
                        case 33: # 50/50
                            pass
                        
                        case 34: # Half end
                            pass
                        
                        case 35: # Starting XI
                            pass
                        
                        case 36: # Tactical shift
                            pass
                        
                        case 37: # Error
                            pass
                        
                        case 38: # Miscontrol
                            pass
                        
                        case 39: # Dribbled past
                            pass
                        
                        case 40: # Injury stoppage
                            pass
                        
                        case 41: # Referee ball-drop
                            pass
                        
                        case 42: # Ball receipt
                            args += "INSERT INTO ball_receipt(event_id, player_id, location) VALUES ('{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"])
                        
                        case 43: # Carry
                            pass

                cursor.execute(args)
        connection.commit()

# DEBUGGING ---------------------------------------- (delete before submitting)
#cursor.execute('SELECT * FROM ball_receipt')
#print(cursor.fetchall())

# CLOSE CONNECTION ---------------------------------
connection.commit()
cursor.close()
connection.close()
print("Script completed successfully.")