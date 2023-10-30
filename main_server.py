from server import Server
from multiprocessing import Process

HOST = '127.0.0.1'
PORT = 65432
INFO = 'version: 0.0.1; creation date: 30.09.2023r'
server = Server(HOST,PORT,INFO)

server_process = Process(target=server.run)
server_process.start()
server.visualization.run()