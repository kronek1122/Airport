import os
import psycopg2
from db_connection_pool import ConnectionPool


class DatabaseManager:
    def __init__(self,database, user, password, host):
        self.connection_pool = ConnectionPool(database, user, password, host)

    
    def add_plane(self, flight_number, status, x, y, z, vector):
        query = '''INSERT INTO flights_log (flight_number, status, x, y, z, velocity_vector)
        VALUES (%s, %s, %s, %s, %s, %s)'''

        values = (flight_number, status, x, y, z, vector)

        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query, values)
            conn.commit()
            msg = 'New plane over the airport'
            self.connection_pool.release_connection(conn)
        except psycopg2.IntegrityError:
            conn.rollback()
            msg = 'Error adding new plane to db'
        return msg


    def get_velocity_vector(self, flight_number):
        query = f'SELECT velocity_vector FROM flights_log WHERE flight_number = {flight_number};'
        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query)
            result = curr.fetchall()
            self.connection_pool.release_connection(conn)
            return result
        except psycopg2.Error as error:
            msg = f'Error getting velocity for flight {flight_number}: {error}'
            return msg


    def change_velocity_vector(self, flight_number, vector):
        query = f'''UPDATE flights_log 
        SET velocity_vector = {vector} 
        WHERE flight_number = {flight_number};'''
        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query)
            conn.commit()
            self.connection_pool.release_connection(conn)
        except psycopg2.Error as error:
            conn.rollback()
            msg = f'Error changing velocity vector: {error}'
            return msg


    def change_status(self, flight_number, status):
        query = f'''UPDATE flights_log 
        SET status = {status} 
        WHERE flight_number = {flight_number};'''
        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query)
            conn.commit()
            self.connection_pool.release_connection(conn)
        except psycopg2.Error as error:
            conn.rollback()
            msg = f'Error changing status: {error}'
            return msg


    def get_appearance_time(self, flight_number):
        query = f'SELECT appearance_time FROM flights_log WHERE flight_number = {flight_number};'
        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query)
            result = curr.fetchall()
            self.connection_pool.release_connection(conn)
            return result
        except psycopg2.Error as error:
            msg = f'Error getting appearance time for flight {flight_number}: {error}'
            return msg


    def get_plane_position(self, flight_number):
        query = f'SELECT (x, y z) FROM flights_log WHERE flight_number = {flight_number};'
        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query)
            result = curr.fetchall()
            self.connection_pool.release_connection(conn)
            return result
        except psycopg2.Error as exp:
            msg = f"Error getting plane coordinate, flight-{flight_number}: {exp}"
            return msg


    def mod_plane_position(self, flight_number, x, y, z):
        query = f'''UPDATE flights_log
        SET x = {x}, y = {y}, z = {z} 
        WHERE flight_number = {flight_number};'''

        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query)
            conn.commit()
            self.connection_pool.release_connection(conn)
            msg = 'Plane position changed'
        except psycopg2.Error as error:
            conn.rollback()
            msg = f'Error changing plane position: {error}'
            return msg
        

    def num_of_plane_over_the_airport(self):
        query = "SELECT COUNT(*) FROM flights_log WHERE STATUS = 'IN_AIR';"
        conn = self.connection_pool.get_connection()
        curr = conn.cursor()
        curr.execute(query)
        result = curr.fetchone()[0]
        self.connection_pool.release_connection(conn)
        return result