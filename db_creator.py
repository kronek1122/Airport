import psycopg2, os
from psycopg2 import errors
from dotenv import load_dotenv

load_dotenv()

database = os.getenv('database')
user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')

# Create Basic Database
conn = psycopg2.connect(user=user, password=password, host = host, port = port)
conn.autocommit = True
c = conn.cursor()

try:
    c.execute('CREATE DATABASE control_tower;')
except errors.DuplicateDatabase:
    pass

conn.close()

#Connect to database
conn = psycopg2.connect(database = database, user=user, password=password, host = host)
c = conn.cursor()

#Create Main Table
query = """CREATE TABLE flight_log (
            log_id SERIAL PRIMARY KEY,
            status VARCHAR,
            appearance_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"""

try:
    c.execute(query)
except errors.DuplicateTable:
    pass


conn.commit()
conn.close()