# Created by Gabriel Martell

'''
This is the template code for the COMP3005 Database Project.
Your task is to ONLY write your SQL queries within the prompted space within each Q_# method (where # is the question number).

Any alterations to the code, such as modifying the time, will be flagged for suspicion of cheating - and thus will be reviewed by the staff and, if need be, the Dean.
To review the Integrity Violation Attributes of Carleton University, please view https://carleton.ca/registrar/academic-integrity/ 
'''

# Imports
import psycopg
import csv
import time
import subprocess
import os

# Name of initial database - this is for initial connections. Do NOT change the name, instead, you should create your initial database with this name.
initial_database = "project_database"

# Name of exported databse - this is for your queries, I would recommend to leave as is. 
export_database_name = "query_database"

# Do NOT Change
dir_path = os.path.dirname(os.path.realpath(__file__))

# IGNORE, Do NOT modify code v
# Drop, then, reload the dbexport.sql
#================================================
def load_database(cursor, conn):
    drop_database(cursor, conn)

    try:
        conn.autocommit = True
        cursor.execute(f"CREATE DATABASE {export_database_name};")
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        conn.autocommit = False
    conn.close()
    
    dbname = export_database_name
    user = 'postgres'
    password = '1234'
    host = 'localhost' 
    port = "5432"
    
    conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    
    try:
        command = f'psql -h {host} -U {user} -d "query_database" -a -f {os.path.join(dir_path, "dbexport.sql")}'
        env = {'PGPASSWORD': password}
        subprocess.run(command, shell=True, check=True, env=env)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while loading the database: {e}")
    
    return conn    

# IGNORE, Do NOT modify code v
# Drop Database
#================================================
def drop_database(cursor, conn):
    try:
        conn.autocommit = True
        cursor.execute(f"DROP DATABASE IF EXISTS {export_database_name};")
        conn.commit()
    except Exception as error:
        print(error)
        pass
    finally:
        conn.autocommit = False

# IGNORE, Do NOT modify code v
# Reconnect to main Database
#================================================
def reconnect(cursor, conn):
    cursor.close()
    conn.close()

    dbname = initial_database
    user = 'postgres'
    password = '1234'
    host = 'localhost' 
    port = "5432"
    return psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# IGNORE, Do NOT modify code v
# Write results
#================================================
def write_csv(execution_time, cursor, conn, i):
    try:
        colnames = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        filename = f"{dir_path}/Q_{i}.csv"

        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            
            # Write column names to the CSV file
            csvwriter.writerow(colnames)
            
            # Write data rows to the CSV file
            csvwriter.writerows(rows)

    except Exception as error:
        execution_time[i-1] = "DNF"
        print(error)
    
#================================================

def Q_1(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    start_time = time.time()
    #==========================================================================
    # Enter query and create .csv here...

    cursor.execute("""
                    SELECT ...
                    FROM ...
                    ...
                    """)
    
    #==========================================================================
    
    end_time = time.time()
    execution_time[0] = (end_time-start_time)

    write_csv(execution_time, cursor, connection, 1)
    return reconnect(cursor, connection)

def Q_2(cursor, conn, execution_time):

    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    start_time = time.time()
    #==========================================================================    
    # Enter query and create .csv here...
    cursor.execute("""

                    """)
    
    #==========================================================================
    
    end_time = time.time()
    execution_time[1] = (end_time-start_time)

    write_csv(execution_time, cursor, connection, 2)
    return reconnect(cursor, connection)
    
def Q_3(cursor, conn, execution_time):

    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    start_time = time.time()

    #==========================================================================    
    # Enter query and create .csv here...
    cursor.execute("""
                    """)

    #==========================================================================
    
    end_time = time.time()
    execution_time[2] = (end_time-start_time)

    write_csv(execution_time, cursor, connection, 3)
    return reconnect(cursor, connection)

def Q_4(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    start_time = time.time()

    #==========================================================================    
    # Enter query and create .csv here...
    cursor.execute("""
                    """)

    #==========================================================================
    
    end_time = time.time()
    execution_time[3] = (end_time-start_time)

    write_csv(execution_time, cursor, connection, 4)
    return reconnect(cursor, connection)

def Q_5(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    start_time = time.time()

    #==========================================================================    
    # Enter query and create .csv here...
    cursor.execute("""
                    """)

    #==========================================================================
    
    end_time = time.time()
    execution_time[4] = (end_time-start_time)

    write_csv(execution_time, cursor, connection, 5)
    return reconnect(cursor, connection)

def Q_6(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    start_time = time.time()

    #==========================================================================    
    # Enter query and create .csv here...
    cursor.execute("""
                    """)

    #==========================================================================
    
    end_time = time.time()
    execution_time[5] = (end_time-start_time)

    write_csv(execution_time, cursor, connection, 6)
    return reconnect(cursor, connection)

def Q_7(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    start_time = time.time()

    #==========================================================================    
    # Enter query and create .csv here...
    cursor.execute("""
                    """)

    #==========================================================================
    
    end_time = time.time()
    execution_time[6] = (end_time-start_time)

    write_csv(execution_time, cursor, connection, 7)
    return reconnect(cursor, connection)

def Q_8(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    start_time = time.time()

    #==========================================================================    
    # Enter query and create .csv here...
    cursor.execute("""
                    """)

    #==========================================================================
    
    end_time = time.time()
    execution_time[7] = (end_time-start_time)

    write_csv(execution_time, cursor, connection, 8)
    return reconnect(cursor, connection)

def Q_9(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    start_time = time.time()

    #==========================================================================    
    # Enter query and create .csv here...
    cursor.execute("""
                    """)
    #==========================================================================

    end_time = time.time()
    execution_time[8] = (end_time-start_time)

    write_csv(execution_time, cursor, connection, 9)
    return reconnect(cursor, connection)

def Q_10(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    start_time = time.time()

    #==========================================================================    
    # Enter query and create .csv here...
    cursor.execute("""
                    """)
    #==========================================================================
    
    end_time = time.time()
    execution_time[9] = (end_time-start_time)

    write_csv(execution_time, cursor, connection, 10)
    return reconnect(cursor, connection)

# IGNORE, Do NOT modify code
#_______________________________________________________
def run_queries(cursor, conn, dbname):

    execution_time = [0,0,0,0,0,0,0,0,0,0]

    conn = Q_1(cursor, conn, execution_time)
    conn = Q_2(cursor, conn, execution_time)
    conn = Q_3(cursor, conn, execution_time)
    conn = Q_4(cursor, conn, execution_time)
    conn = Q_5(cursor, conn, execution_time)
    conn = Q_6(cursor, conn, execution_time)
    conn = Q_7(cursor, conn, execution_time)
    conn = Q_8(cursor, conn, execution_time)
    conn = Q_9(cursor, conn, execution_time)
    conn = Q_10(cursor, conn, execution_time)

    for i in range(10):
        print(execution_time[i])

try:
    if __name__ == "__main__":

        dbname = initial_database
        user = 'postgres'
        password = '1234'
        host = 'localhost' 
        port = "5432"

        conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cursor = conn.cursor()
        
        run_queries(cursor, conn, dbname)
except Exception as error:
    print(error)
    #print("[ERROR]: Failure to connect to database.")
#_______________________________________________________
