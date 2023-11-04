import socket as s
import time
import json
from plane_generator import PlaneGenerator

class PlaneSocket:
    HOST = '127.0.0.1'
    PORT = 65432
    FUEL_SUPPLY = (3*3600)

    def __init__(self, flight_num):
        self.client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        self.in_air = True
        self.flight_num = flight_num
        self.position = PlaneGenerator().position_generator()
        self.position_x = self.position[0]
        self.position_y = self.position[1]
        self.position_z = self.position[2]
        self.velocity = PlaneGenerator().vector_generator()
        self.fuel_empty_time = time.time() + self.FUEL_SUPPLY
        self.is_fuel = True
        self.status = 'IN_AIR'

    def data_dictionary(self):
        flight_data = {'flight_number':self.flight_num,
                       'position_x':self.position_x,
                       'position_y':self.position_y,
                       'position_z':self.position_z,
                       'velocity_vector':self.velocity,
                       'IS_FUEL':self.is_fuel,
                       'status':self.status}
        return flight_data


    def json_data_converter(self):
        flight_data = self.data_dictionary()
        self.json_flight_data = json.dumps(flight_data)
        return self.json_flight_data


    def vector_update(self, data):
        self.velocity = data['velocity_vector']


    def position_update(self):
        self.position_x += self.velocity[0]
        self.position_y += self.velocity[1]
        self.position_z += self.velocity[2]


    def fuel_gauge_check(self):
        if time.time() > self.fuel_empty_time:
            self.is_fuel = False
        else: self.is_fuel = True


    def send_socket(self):
        while True:
            flight_data = self.data_dictionary()
            self.fuel_gauge_check()
            if flight_data['IS_FUEL'] is False:
                self.status = 'Plane crashed'
                flight_data_json = self.json_data_converter()
                self.client_socket.sendall(flight_data_json.encode('utf8'))
                break

            flight_data_json = self.json_data_converter()
            self.client_socket.sendall(flight_data_json.encode('utf8'))
            received_data = self.client_socket.recv(1024).decode('utf8')
            received_dict = json.loads(received_data)

            print(f'''
                dane samolotu: {flight_data}
                otrzymane dane: {received_dict}''')

            if received_dict['msg'] == 'to many planes in the air' or received_dict['msg'] == 'landed' or received_dict['msg'] == 'Plane crashed':
                break
            else:
                self.vector_update(received_dict)
                self.position_update()

            time.sleep(1)
