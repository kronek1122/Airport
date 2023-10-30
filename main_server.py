from server import Server
from multiprocessing import Process

HOST = '127.0.0.1'
PORT = 65432
INFO = 'version: 0.0.1; creation date: 30.09.2023r'
server = Server(HOST,PORT,INFO)

animation_process = Process(target=server.visualization.run)
animation_process.start()
server.run()