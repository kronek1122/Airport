import socket as s
from plane_manager import PlaneManager

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()


    def json_unpacking(self, data):
        unpacking_data = []
        unpacking_data = data.split(' ')
        return unpacking_data

    def run(self):
        connection, address = self.server_socket.accept()
        print(f'Connected by {address}')

        while True:
            query = connection.recv(1024).decode('utf8')

            if not query:
                break
        
            connection.send(PlaneManager(query).new_plane().encode('utf8'))