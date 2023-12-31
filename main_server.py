from server import Server
from multiprocessing import Process

HOST = '127.0.0.1'
PORT = 65432
INFO = 'version: 0.1.0; creation date: 30.09.2023r'
server = Server(HOST,PORT,INFO)

server_process = Process(target=server.run)
server_process.start()
server_procces_2 = Process(target=server.visualization.run)
server_procces_2.start()
server_procces_3 = Process(target=server.information)
server_procces_3.start()
