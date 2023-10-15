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


    def run(self):
        connection, address = self.server_socket.accept()
        print(f'Connected by {address}')

        while True:
            query = connection.recv(1024).decode('utf8')
            if query:
                received_data = json.loads(query)
                plane_manager = PlaneManager(received_data)
                response_data = plane_manager.plane_signal()
                print(response_data)
                json_response_data = json.dumps(response_data)
                connection.sendall(json_response_data.encode('utf8'))

