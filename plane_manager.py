'''Manage planes script'''
from db_connection_pool import ConnectionPool

class PlaneManager:
    
    def __init__(self, dictionary:dict, connection):
        self.flight_number = dictionary['flight_number']
        self.position_x = dictionary['position x']
        self.position_y = dictionary['position y']
        self.position_z = dictionary['position_z']
        self.status = dictionary['status']
        self.velocity = dictionary['velocity_vector']
        self.velocity_x = self.velocity[0]
        self.velocity_y = self.velocity[1]
        self.velocity_z = self.velocity[2]
        self.db = connection

    def plane_signal(self):
        if self.position_z == 0:
            self.db.change_status(self.flight_number, 'LANDED')
            result = {'msg':'landed',
                      'status':'overloaded'}
        else:
            if self.db.num_of_planes_over_the_airport() < 100 or self.db.plane_status(self.flight_number)=='IN_AIR':
                msg = self.db.add_plane(self.flight_number, self.status, self.position_x, self.position_y, self.position_z, self.velocity_x, self.velocity_y, self.velocity_z)
                if msg['msg'] == 'Error adding new plane to db':
                    self.db.change_plane_information(self.flight_number, self.status, self.position_x, self.position_y, self.position_z, self.velocity_x, self.velocity_y, self.velocity_z)
                    result = self.control_tower_system()
                else:
                    result = self.control_tower_system()
            else: 
                result = {'msg':'to many planes in the air',
                          'status':'overloaded'}
        return result


    def control_tower_system(self):
        #dodać system sterowanie ruchem
        result = self.dictionary_data_pack()
        return result


    def dictionary_data_pack(self):
        result = {'msg':'change direction',
                  'status':"IN_AIR",
                  'velocity_vector':self.velocity}
        return result