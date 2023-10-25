import psycopg2, os
from psycopg2 import errors
from dotenv import load_dotenv

load_dotenv()

postgres_config_str = os.getenv('POSTGRES_CONFIG')
postgres_config = eval(postgres_config_str)

try:
    conn = psycopg2.connect(**postgres_config)
    conn.autocommit = True
    c = conn.cursor()

    c.execute('DROP DATABASE IF EXISTS control_tower;')

except psycopg2.Error as e:
    print("Database delete error", e)

finally:
    if conn is not None:
        conn.close()