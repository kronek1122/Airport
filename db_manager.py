import os
import psycopg2
from db_connection_pool import ConnectionPool


class DatabaseManager:
    def __init__(self,database, user, password, host):
        self.connection_pool = ConnectionPool(database, user, password, host)

    
    def add_plane(self, flight_number, status, x, y, z, vector):
        flight_log_query = "INSERT INTO flight_log status VALUE %s;"

        plane_table = f"""CREATE TABLE {flight_number} (
                        plane_id SERIAL PRIMARY KEY,
                        log_id INT REFERENCE flight_log(log_id),
                        x FLOAT,
                        y FLOAT,
                        z FLOAT,
                        velocity_vector NUMERIC[]"""
        
        plane_table_query = f"""INSERT INTO {flight_number} (x, y, z, velocity_vector) VALUES ({x}, {y}, {z}, {vector})"""

        try: 
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(flight_log_query, status)
            curr.execute(plane_table)
            curr.execute(plane_table_query)         #może rozbić funkcję na dwie niezależne (jedna dodająca do tabeli głownej druga tworząca i modyfikująca dane o samolocie)
            conn.commit()
            msg = 'New plane over the airport'
            self.connection_pool.release_connection(conn)
        except psycopg2.Error as exp:
            conn.rollback()
            msg = f"Error adding plane to db : {exp}"
        return msg
    
    
    def get_velocity_vector(self, flight_number):
        pass


    def change_velocity_vector(self, vector):
        pass


    def get_appearance_time(self):
        pass


    def mod_plane_position(self, flight_number):
        pass