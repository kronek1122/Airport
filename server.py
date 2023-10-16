import socket as s
import json
import threading
from plane_manager import PlaneManager

class Server:

    def __init__(self, host, port, info):
        self.host = host
        self.port = port
        self.info = info
        self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()


    def handle_client(self, connection, address):
        print(f'Connected by {address}')

        while True:
            query = connection.recv(1024).decode('utf8')
            if not query:
                break
            received_data = json.loads(query)
            plane_manager = PlaneManager(received_data)
            response_data = plane_manager.plane_signal()
            print(response_data)
            json_response_data = json.dumps(response_data)
            connection.sendall(json_response_data.encode('utf8'))

    def run(self):
        while True:
            connection, address = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(connection, address))
            thread.start()

