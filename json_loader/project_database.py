import psycopg
import json
from pathlib import Path

# ESTABLISH CONNECTION -----------------------------

# TA: Change as needed
user = 'postgres'
password = '1234'
host = 'localhost'
port = "5432"
data_directory = Path('/media/sf_VM_Folder/data/') # Where the StatsBomb data folder is (i.e. '/media/sf_VM_Folder/data/')

# DROP then CREATE project_database (in case script was ran previously)
connection = psycopg.connect(dbname='postgres', user=user, password=password, host=host, port=port)
connection.autocommit = True
cursor = connection.cursor()
cursor.execute('DROP DATABASE IF EXISTS project_database')
cursor.execute("""
                CREATE DATABASE project_database
                WITH OWNER "postgres"
                ENCODING 'UTF8'
                LC_COLLATE = 'en_US.UTF-8'
                LC_CTYPE = 'en_US.UTF-8'
                TEMPLATE template0;
               """)

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
        match_id INT NOT NULL,
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
        PRIMARY KEY (camera_on_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id)
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
        duration DECIMAL,
        recipient_id INT,
        length DECIMAL,
        angle DECIMAL,
        height VARCHAR(20),
        body_part VARCHAR(20),
        technique VARCHAR(20),
        shot_assist BOOLEAN DEFAULT 'false',
        outcome VARCHAR(20),
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
        duration DECIMAL,
        xg DECIMAL,
        first_time BOOLEAN DEFAULT 'false',
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
               
    CREATE TABLE pressure (
        pressure_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        duration DECIMAL,
        PRIMARY KEY (pressure_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)    
    );
               
    CREATE TABLE half_start (
        half_start_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        duration DECIMAL,
        PRIMARY KEY (half_start_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id)   
    );
               
    CREATE TABLE substitution (
        substitution_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        duration DECIMAL,
        outcome VARCHAR(20),
        replacement_id INT NOT NULL,
        PRIMARY KEY (substitution_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id), 
        FOREIGN KEY (replacement_id) REFERENCES player(player_id)
    );
               
    CREATE TABLE own_goal_against (
        own_goal_against_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        PRIMARY KEY (own_goal_against_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id)
    );
               
    CREATE TABLE foul_won (
        foul_won_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        duration DECIMAL,
        PRIMARY KEY (foul_won_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)
    );
               
    CREATE TABLE foul_committed (
        foul_committed_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        duration DECIMAL,     
        PRIMARY KEY (foul_committed_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)       
    );
               
    CREATE TABLE goalkeeper (
        goalkeeper_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        end_location VARCHAR(20),
        duration DECIMAL,    
        type VARCHAR(30),
        position VARCHAR(30),
        PRIMARY KEY (goalkeeper_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)       
    );
               
    CREATE TABLE bad_behaviour (
        bad_behaviour_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        duration DECIMAL,   
        card_type VARCHAR(20),
        PRIMARY KEY (bad_behaviour_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)       
    );
               
    CREATE TABLE own_goal_for (
        own_goal_for_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        PRIMARY KEY (own_goal_for_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id)
    );
               
    CREATE TABLE player_on (
        player_on_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        PRIMARY KEY (player_on_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)
    );
               
    CREATE TABLE player_off (
        player_off_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        PRIMARY KEY (player_off_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)
    );
               
    CREATE TABLE shield (
        shield_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        PRIMARY KEY (shield_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)
    );
               
    CREATE TABLE _50_50 (
        _50_50_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        outcome VARCHAR(30),
        PRIMARY KEY (_50_50_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)
    );
               
    CREATE TABLE half_end (
        half_end_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        PRIMARY KEY (half_end_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id)
    );
               
    CREATE TABLE error (
        error_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        PRIMARY KEY (error_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)
    );
               
    CREATE TABLE miscontrol (
        miscontrol_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        PRIMARY KEY (miscontrol_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)
    );
               
    CREATE TABLE dribbled_past (
        dribbled_past_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        PRIMARY KEY (dribbled_past_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)
    );
               
    CREATE TABLE injury_stoppage (
        injury_stoppage_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        PRIMARY KEY (injury_stoppage_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id)
    );
               
    CREATE TABLE referee_ball_drop (
        referee_ball_drop_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        location VARCHAR(20),
        duration DECIMAL,   
        PRIMARY KEY (referee_ball_drop_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id)    
    );
               
    CREATE TABLE carry (
        carry_id SERIAL,
        event_id VARCHAR(40) NOT NULL,
        player_id INT NOT NULL,
        location VARCHAR(20),
        duration DECIMAL,   
        PRIMARY KEY (carry_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id)       
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
                    cursor.execute("INSERT INTO lineup(match_id) VALUES (%s)", (match_number,))
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
                            args += "INSERT INTO camera_on(event_id) VALUES ('{}');".format(event["id"])

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
                            if ("key_pass_id" in event["shot"] and "first_time" in event["shot"]):
                                args += "INSERT INTO shot(event_id, player_id, location, end_location, duration, xg, first_time, outcome, body_part, technique, type, key_pass_id) VALUES ('{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["shot"]["end_location"], event["duration"], event["shot"]["statsbomb_xg"], event["shot"]["first_time"], event["shot"]["outcome"]["name"], event["shot"]["body_part"]["name"], event["shot"]["technique"]["name"], event["shot"]["type"]["name"], event["shot"]["key_pass_id"])
                            elif ("key_pass_id" in event["shot"]):
                                args += "INSERT INTO shot(event_id, player_id, location, end_location, duration, xg, outcome, body_part, technique, type, key_pass_id) VALUES ('{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["shot"]["end_location"], event["duration"], event["shot"]["statsbomb_xg"], event["shot"]["outcome"]["name"], event["shot"]["body_part"]["name"], event["shot"]["technique"]["name"], event["shot"]["type"]["name"], event["shot"]["key_pass_id"])
                            elif ("first_time" in event["shot"]):
                                args += "INSERT INTO shot(event_id, player_id, location, end_location, duration, xg, first_time, outcome, body_part, technique, type) VALUES ('{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["shot"]["end_location"], event["duration"], event["shot"]["statsbomb_xg"], event["shot"]["first_time"], event["shot"]["outcome"]["name"], event["shot"]["body_part"]["name"], event["shot"]["technique"]["name"], event["shot"]["type"]["name"])
                            else:
                                args += "INSERT INTO shot(event_id, player_id, location, end_location, duration, xg, outcome, body_part, technique, type) VALUES ('{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["shot"]["end_location"], event["duration"], event["shot"]["statsbomb_xg"], event["shot"]["outcome"]["name"], event["shot"]["body_part"]["name"], event["shot"]["technique"]["name"], event["shot"]["type"]["name"])
                        
                        case 17: # Pressure
                            args += "INSERT INTO pressure(event_id, player_id, location, duration) VALUES ('{}', '{}', '{}', {});".format(event["id"], event["player"]["id"], event["location"], event["duration"])
                        
                        case 18: # Half start
                             args += "INSERT INTO half_start(event_id, duration) VALUES ('{}', {});".format(event["id"], event["duration"])
                        
                        case 19: # Substitution
                            args += "INSERT INTO substitution(event_id, player_id, duration, outcome, replacement_id) VALUES ('{}', '{}', {}, '{}', '{}');".format(event["id"], event["player"]["id"], event["duration"], event["substitution"]["outcome"]["name"], event["substitution"]["replacement"]["id"])
                        
                        case 20: # Own goal against
                            args += "INSERT INTO own_goal_for(event_id) VALUES ('{}');".format(event["id"])
                        
                        case 21: # Foul won
                            args += "INSERT INTO foul_won(event_id, player_id, location, duration) VALUES ('{}', '{}', '{}', {});".format(event["id"], event["player"]["id"], event["location"], event["duration"])

                        case 22: # Foul committed
                            args += "INSERT INTO foul_committed(event_id, player_id, location, duration) VALUES ('{}', '{}', '{}', {});".format(event["id"], event["player"]["id"], event["location"], event["duration"])
                        
                        case 23: # Goal keeper
                            if ("location" in event):
                                if ("end_location" in event["goalkeeper"] and "position" in event["goalkeeper"]):
                                    args += "INSERT INTO goalkeeper(event_id, player_id, location, end_location, duration, type, position) VALUES ('{}', '{}', '{}', '{}', {}, '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["goalkeeper"]["end_location"], event["duration"], event["goalkeeper"]["type"]["name"], event["goalkeeper"]["position"]["name"])
                                elif ("end_location" in event["goalkeeper"]):
                                    args += "INSERT INTO goalkeeper(event_id, player_id, location, end_location, duration, type) VALUES ('{}', '{}', '{}', '{}', {}, '{}');".format(event["id"], event["player"]["id"], event["location"], event["goalkeeper"]["end_location"], event["duration"], event["goalkeeper"]["type"]["name"])
                                elif ("position" in event["goalkeeper"]):
                                    args += "INSERT INTO goalkeeper(event_id, player_id, location, duration, type, position) VALUES ('{}', '{}', '{}', {}, '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["duration"], event["goalkeeper"]["type"]["name"], event["goalkeeper"]["position"]["name"])                
                                else:
                                    args += "INSERT INTO goalkeeper(event_id, player_id, location, duration, type) VALUES ('{}', '{}', '{}', {}, '{}');".format(event["id"], event["player"]["id"], event["location"], event["duration"], event["goalkeeper"]["type"]["name"])  
                            else:
                                if ("end_location" in event["goalkeeper"] and "position" in event["goalkeeper"]):
                                    args += "INSERT INTO goalkeeper(event_id, player_id, end_location, duration, type, position) VALUES ('{}', '{}', '{}', {}, '{}', '{}');".format(event["id"], event["player"]["id"], event["goalkeeper"]["end_location"], event["duration"], event["goalkeeper"]["type"]["name"], event["goalkeeper"]["position"]["name"])
                                elif ("end_location" in event["goalkeeper"]):
                                    args += "INSERT INTO goalkeeper(event_id, player_id, end_location, duration, type) VALUES ('{}', '{}', '{}', {}, '{}');".format(event["id"], event["player"]["id"], event["goalkeeper"]["end_location"], event["duration"], event["goalkeeper"]["type"]["name"])
                                elif ("position" in event["goalkeeper"]):
                                    args += "INSERT INTO goalkeeper(event_id, player_id, duration, type, position) VALUES ('{}', '{}', {}, '{}', '{}');".format(event["id"], event["player"]["id"], event["duration"], event["goalkeeper"]["type"]["name"], event["goalkeeper"]["position"]["name"])                
                                else:
                                    args += "INSERT INTO goalkeeper(event_id, player_id, duration, type) VALUES ('{}', '{}', {}, '{}');".format(event["id"], event["player"]["id"], event["duration"], event["goalkeeper"]["type"]["name"])  
          
                        case 24: # Bad behaviour
                            args += "INSERT INTO bad_behaviour(event_id, player_id, duration, card_type) VALUES ('{}', '{}', {}, '{}');".format(event["id"], event["player"]["id"], event["duration"], event["bad_behaviour"]["card"]["name"])
                        
                        case 25: # Own goal for
                            args += "INSERT INTO own_goal_for(event_id) VALUES ('{}');".format(event["id"])

                        case 26: # Player on
                            args += "INSERT INTO player_on(event_id, player_id) VALUES ('{}', {});".format(event["id"], event["player"]["id"])
                        
                        case 27: # Player off
                            args += "INSERT INTO player_off(event_id, player_id) VALUES ('{}', {});".format(event["id"], event["player"]["id"])
                        
                        case 28: # Shield
                            args += "INSERT INTO shield(event_id, player_id, location) VALUES ('{}', {}, '{}');".format(event["id"], event["player"]["id"], event["location"])
                        
                        case 30: # Pass     
                            # Too many optional components of a pass to make an if statement for each combination
                            event_pass = event["pass"]

                            parameters = "event_id, player_id, location, end_location, duration, length, angle, height"
                            values = [event["id"], event["player"]["id"], event["location"], event["pass"]["end_location"], event["duration"], event["pass"]["length"], event["pass"]["angle"], event["pass"]["height"]["name"]]

                            if ("recipient" in event_pass): 
                                parameters += ", recipient_id"
                                values.append(event["pass"]["recipient"]["id"])

                            if ("body_part" in event_pass):
                                parameters += ", body_part"
                                values.append(event["pass"]["body_part"]["name"])

                            if ("technique" in event_pass):
                                parameters += ", technique"
                                values.append(event["pass"]["technique"]["name"])

                            if ("shot_assist" in event_pass):
                                parameters += ", shot_assist"
                                values.append(event["pass"]["shot_assist"])

                            if ("outcome" in event_pass):
                                parameters += ", outcome"
                                values.append(event["pass"]["outcome"]["name"])

                            if ("type" in event_pass):
                                parameters += ", type"
                                values.append(event["pass"]["type"]["name"])

                            args += "INSERT INTO pass(" + parameters + ") VALUES (" 
                            for i in range(len(values)):
                                if (i == len(values)-1): # Don't put comma after last parameter
                                    args += "'{}'".format(values[i])
                                else:
                                    args += "'{}',".format(values[i])
                            args += ");"

                        case 33: # 50/50
                            args += "INSERT INTO _50_50(event_id, player_id, location, outcome) VALUES ('{}', {}, '{}', '{}');".format(event["id"], event["player"]["id"], event["location"], event["50_50"]["outcome"]["name"])
                        
                        case 34: # Half end
                            args += "INSERT INTO half_end(event_id) VALUES ('{}');".format(event["id"])
                        
                        case 37: # Error
                            args += "INSERT INTO error(event_id, player_id, location) VALUES ('{}', {}, '{}');".format(event["id"], event["player"]["id"], event["location"])
                        
                        case 38: # Miscontrol
                            args += "INSERT INTO miscontrol(event_id, player_id, location) VALUES ('{}', {}, '{}');".format(event["id"], event["player"]["id"], event["location"])
                        
                        case 39: # Dribbled past
                            args += "INSERT INTO dribbled_past(event_id, player_id, location) VALUES ('{}', {}, '{}');".format(event["id"], event["player"]["id"], event["location"])
                        
                        case 40: # Injury stoppage
                            args += "INSERT INTO injury_stoppage(event_id) VALUES ('{}');".format(event["id"])
                        
                        case 41: # Referee ball-drop
                            args += "INSERT INTO referee_ball_drop(event_id, location, duration) VALUES ('{}', '{}', {});".format(event["id"], event["location"], event["duration"])
                        
                        case 42: # Ball receipt
                            args += "INSERT INTO ball_receipt(event_id, player_id, location) VALUES ('{}', '{}', '{}');".format(event["id"], event["player"]["id"], event["location"])
                        
                        case 43: # Carry
                            args += "INSERT INTO carry(event_id, player_id, location, duration) VALUES ('{}', '{}', '{}', {});".format(event["id"], event["player"]["id"], event["location"], event["duration"])

                cursor.execute(args)
        connection.commit()

# DEBUGGING ----------------------------------------
#cursor.execute('SELECT * FROM ball_receipt')
#print(cursor.fetchall())

# CLOSE CONNECTION ---------------------------------
connection.commit()
cursor.close()
connection.close()