import socket as s


class Server:

    def __init__(self, host, port):
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

            query_list = self.json_unpacking(query)
        
            connection.send("""funkcja tworząca i zarządzająca samolotami""").encode('utf8'))