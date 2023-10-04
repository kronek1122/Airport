import os
import psycopg2
from db_connection_pool import ConnectionPool


class DatabaseManager:
    def __init__(self,database, user, password, host):
        self.connection_pool = ConnectionPool(database, user, password, host)

    
    def add_plane(self, flight_number, status, x, y, z, vector):
        query = f"""INSERT INTO flights_log (flight_number, status, x, y, z, velocity_vector)
        VALUES ({flight_number}, {status}, {x}, {y}, {z}, {vector});"""
        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query)
            conn.commit()
            msg = 'New plane over the airport'
            self.connection_pool.release_connection(conn)
        except psycopg2.Error as exp:
            conn.rollback()
            msg = f"Error adding plane to db : {exp}"
        return msg


    def get_velocity_vector(self, flight_number):
        query = f"SELECT velocity_vector FROM flights_log WHERE flight_number = {flight_number};"
        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query)
            result = curr.fetchall()
            self.connection_pool.release_connection(conn)
            return result
        except psycopg2.Error as exp:
            msg = f"Error getting velocity for flight {flight_number}: {exp}"
            return msg

    def change_velocity_vector(self, vector, flight_number):
        query = f"""UPDATE flights_log 
        SET velocity_vector = {vector} 
        WHERE flight_number = {flight_number};"""
        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query)
            conn.commit()
        except psycopg2.Error as exp:
            conn.rollback()
            msg = f"Error changing velocity vector: {exp}"
            return msg


    def get_appearance_time(self, flight_number):
        query = f"SELECT appearance_time FROM flights_log WHERE flight_number = {flight_number};"
        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query)
            result = curr.fetchall()
            self.connection_pool.release_connection(conn)
            return result
        except psycopg2.Error as exp:
            msg = f"Error getting appearance time for flight {flight_number}: {exp}"
            return msg


    def get_plane_position(self, flight_number):
        query = f"SELECT (x, y z) FROM flights_log WHERE flight_number = {flight_number};"
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
        query = f"""UPDATE flights_log
        SET (x ,y ,z) = {x},{y},{z} 
        WHERE flight_number = {flight_number};"""

        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query)
            conn.commit()
        except psycopg2.Error as exp:
            conn.rollback()
            msg = f"Error changing velocity vector: {exp}"
            return msg