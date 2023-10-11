import socket as s
import time
import random


class PlaneSocket:
    HOST = '127.0.0.1'
    PORT = 65432

    def __init__(self):
        self.client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        self.flight_number_gen = self.flight_number_generator()
    
    def flight_number_generator(self):
        num = 1
        while True:
            yield num
            num += 1

    def send_socket(self):
        while True:
            flight_num = next(self.flight_number_gen)
            self.client_socket.sendall(str(flight_num).encode('utf8'))
            data = self.client_socket.recv(1024).decode('utf8')
            print(data)
            time.sleep(random.randint(1,7))


if __name__ == '__main__':
    client = PlaneSocket()
    client.send_socket()

