import psycopg2, os
from psycopg2 import errors
from dotenv import load_dotenv

load_dotenv()

postgres_config_str = os.getenv('POSTGRES_CONFIG')
postgres_config = eval(postgres_config_str)

postgres_config_db_str = os.getenv('POSTGRES_CONFIG_DB')
postgres_config_db = eval(postgres_config_db_str)

# Create Basic Database
conn = psycopg2.connect(**postgres_config)
conn.autocommit = True
c = conn.cursor()

try:
    c.execute('CREATE DATABASE control_tower;')
except errors.DuplicateDatabase:
    pass

conn.close()

#Connect to database
conn = psycopg2.connect(**postgres_config_db)
c = conn.cursor()

#Create Main Table
query = """CREATE TABLE flights_log (
            flight_number INT UNIQUE,
            status VARCHAR,
            appearance_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            x INT,
            y INT,
            z INT,
            velocity_vector_x INT,
            velocity_vector_y INT,
            velocity_vector_z INT);"""
        

try:
    c.execute(query)
except errors.DuplicateTable:
    pass


conn.commit()
conn.close()