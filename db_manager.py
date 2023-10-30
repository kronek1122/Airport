import os
import psycopg2
from db_connection_pool import ConnectionPool


class DatabaseManager:
    def __init__(self,database, user, password, host):
        self.connection_pool = ConnectionPool(database, user, password, host)

    
    def add_plane(self, flight_number:int, status:str, x:int, y:int, z:int, vector_x:int, vector_y:int, vector_z:int):
        query = '''INSERT INTO flights_log (flight_number, status, x, y, z, velocity_vector_x, velocity_vector_y, velocity_vector_z)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''

        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            values = (flight_number, status, x, y, z, vector_x, vector_y, vector_z)
            curr.execute(query,values)
            conn.commit()
            msg = {'msg': 'New plane over the airport',
                   'error': False}
        except psycopg2.IntegrityError as error:
            conn.rollback()
            msg = {'msg': 'Error adding new plane to db',
                   'error': True,
                   'error_msg': f"{error}"}
        finally:
            self.connection_pool.release_connection(conn)
        return msg


    def change_status(self, flight_number:int, status:str):
        query = '''UPDATE flights_log 
        SET status = %s 
        WHERE flight_number = %s;'''
        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query,(status,flight_number))
            conn.commit()
            msg = {'msg': 'Changed status',
                   'error': False}
        except psycopg2.Error as error:
            conn.rollback()
            msg = {'msg': 'Error changing status:',
                   'error': True,
                   'error_msg': f"{error}"}
        finally:
            self.connection_pool.release_connection(conn)
        return msg


    def change_plane_information(self, flight_number:int, status:str, x:int, y:int, z:int, vector_x:int, vector_y:int, vector_z:int)-> dict:
        query = '''UPDATE flights_log
        SET status = %s, x = %s, y = %s, z = %s , velocity_vector_x = %s, velocity_vector_y = %s, velocity_vector_z = %s
        WHERE flight_number = %s;'''

        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            values = (status, x, y, z, vector_x, vector_y, vector_z, flight_number)
            curr.execute(query,values)
            conn.commit()
            msg = {'msg': 'Plane position and velocity vector changed',
                   'error': False}
        except psycopg2.Error as error:
            conn.rollback()
            msg = {'msg': 'Error changing plane position and velocity vector:',
                   'error': True,
                   'error_msg': f"{error}"}
        finally:
            self.connection_pool.release_connection(conn)
        return msg
        

    def num_of_planes_over_the_airport(self):
        query = "SELECT COUNT(*) FROM flights_log WHERE status = 'IN_AIR';"
        conn = self.connection_pool.get_connection()
        curr = conn.cursor()
        curr.execute(query)
        result = curr.fetchone()[0]
        self.connection_pool.release_connection(conn)
        return result
    

    def plane_status(self,flight_number:int):
        query = "SELECT status FROM flights_log WHERE flight_number = %s;"
        conn = self.connection_pool.get_connection()
        curr = conn.cursor()
        curr.execute(query, (flight_number,))
        result = curr.fetchone()
        if result:
            result = result[0]
        self.connection_pool.release_connection(conn)
        return result


    def get_coordinates(self):
        query = "SELECT x, y, z, flight_number FROM flights_log WHERE status = 'IN_AIR';"

        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query)
            result = curr.fetchall()
            coordinates = [(x, y, z, flight_number) for x, y, z, flight_number in result]
        except psycopg2.Error as error:
            coordinates = []
            print(f"Error retrieving coordinates: {error}")
        finally:
            self.connection_pool.release_connection(conn)
        return coordinates

