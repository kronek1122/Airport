import threading
import time
from queue import Queue, Empty, Full
import psycopg2


class ConnectionPool:
    def __init__(self, database, user, password, host):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.min_connections = 2
        self.max_connections = 50
        self.connections_queue = Queue(maxsize=self.max_connections)
        self.semaphore = threading.Semaphore()
        self.connections_released = 0
        self.active_connections = 0
        self.initialize_connections()

        self.connections_check = threading.Thread(target=self.connections_manager)
        self.connections_check.daemon = True
        self.connections_check.start()

    def initialize_connections(self):
        for _ in range(self.min_connections):
            self.create_connection()


    def create_connection(self):
        with self.semaphore:
            if (self.connections_queue.qsize() + self.active_connections) < self.max_connections:
                try:
                    connection = psycopg2.connect(database = self.database, user = self.user, password = self.password, host =self.host)
                    self.connections_queue.put(connection)
                except Exception as exp:
                    print("Error creating connection:", exp)
                    return None
            else:
                return None


    def get_connection(self):
        try:
            self.create_connection()
            connection = self.connections_queue.get(timeout=2)
            self.active_connections +=1
        except Empty:
            while True:
                try:
                    connection = self.connections_queue.get(timeout=2)
                    self.active_connections +=1
                    break
                except Empty:
                    pass
        return connection


    def connections_manager(self):
        while True:
            while self.connections_queue.qsize()>self.min_connections:
                connection = self.connections_queue.get()
                try:
                    connection.close()
                except Exception as error:
                    print("Error:", error)
            time.sleep(1)


    def release_connection(self, connection):
        with self.semaphore:           
            try:
                self.connections_queue.put(connection, block=False)
                self.active_connections -=1
                self.connections_released += 1            
            except Full:
                try:
                    connection.close()
                    self.active_connections -=1
                    self.connections_released += 1
                except Exception as error:
                    print("Error:", error)