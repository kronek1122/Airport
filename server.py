import socket as s
import json
from plane_manager import PlaneManager

class Server:

    def __init__(self, host, port, info):
        self.host = host
        self.port = port
        self.info = info
        self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def json_data_converter(self, data):
        self.json_flight_data = json.dumps(data)
        return self.json_flight_data

    def run(self):
        connection, address = self.server_socket.accept()
        print(f'Connected by {address}')

        while True:
            query = connection.recv(1024).decode('utf8')
            received_dict = json.loads(query)
            data = PlaneManager(received_dict).plane_signal()
            json_data = self.json_data_converter(data)
            connection.sendall(json_data.encode('utf8'))