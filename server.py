import os
import socket as s
import json
import threading
from plane_manager import PlaneManager
from db_manager import DatabaseManager
from visualization import Visualization3D
from dotenv import load_dotenv

load_dotenv()

class Server:

    def __init__(self, host, port, info):
        postgres_config_str = os.getenv('POSTGRES_CONFIG_DB')
        self.postgres_config = eval(postgres_config_str)
        self.host = host
        self.port = port
        self.info = info
        self.active_threads = 0
        self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.db_plane_manager = DatabaseManager(**self.postgres_config)
        self.db_visualization = DatabaseManager(**self.postgres_config)
        self.visualization = Visualization3D(self.db_visualization)


    def handle_client(self, connection, address):
        print(f'Connected by {address}')

        while True:
            query = connection.recv(1024).decode('utf8')
            if not query:
                break
            received_data = json.loads(query)
            plane_manager = PlaneManager(received_data, self.db_plane_manager)
            response_data = plane_manager.plane_signal()
            json_response_data = json.dumps(response_data)
            connection.sendall(json_response_data.encode('utf8'))

    def run(self):
        while True:
            connection, address = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(connection, address))
            thread.start()
            self.active_threads +=1