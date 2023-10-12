from server import Server

HOST = '127.0.0.1'
PORT = 65432
INFO = 'version: 0.0.1; creation date: 30.09.2023r'
server = Server(HOST,PORT)

server.run()