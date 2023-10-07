import socket as s
import time
import random
from plane_generator import PlaneGenerator


class PlaneSocket:
    HOST = '127.0.0.1'
    PORT = 65432

    def __init__(self):
        self.client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
            

    def send_socket(self):
        while True:
            command = PlaneGenerator().new_plane().encode('utf8')
            self.client_socket.sendall(command)
            data = self.client_socket.recv(1024).decode('utf8')
            print(data)
            time.sleep(random.randint(1,7))


if __name__ == '__main__':
    client = PlaneSocket()
    client.send_socket()

