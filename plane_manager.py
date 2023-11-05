'''Manage planes script'''
from control_tower import ControlTower

class PlaneManager:
    
    def __init__(self, dictionary:dict, connection):
        self.dictionary = dictionary
        self.flight_number = self.dictionary['flight_number']
        self.position_x = self.dictionary['position_x']
        self.position_y = self.dictionary['position_y']
        self.position_z = self.dictionary['position_z']
        self.status = self.dictionary['status']
        self.velocity = self.dictionary['velocity_vector']
        self.velocity_x = self.velocity[0]
        self.velocity_y = self.velocity[1]
        self.velocity_z = self.velocity[2]
        self.db = connection

    def plane_signal(self):
        if self.position_z == 0:
            self.db.change_status(self.flight_number, 'LANDED')
            result = {'msg':'landed',
                      'status':'LANDED'}

        elif self.position_z < 0:
            result = {'msg':'plane crashed',
                      'status':'CRASHED'}

        else:
            if self.db.get_num_of_planes_by_status('IN_AIR') < 100 or self.db.plane_status(self.flight_number)=='IN_AIR':
                msg = self.db.add_plane(self.flight_number, self.status, self.position_x, self.position_y, self.position_z, self.velocity_x, self.velocity_y, self.velocity_z)
                if msg['msg'] == 'Error adding new plane to db':
                    self.db.change_plane_information(self.flight_number, self.status, self.position_x, self.position_y, self.position_z, self.velocity_x, self.velocity_y, self.velocity_z)
                    result = self.control_tower_system()
                else:
                    result = self.control_tower_system()

            else: 
                result = {'msg':'to many planes in the air',
                          'status':'REDIRECTED'}
                self.status = result['status']
                msg = self.db.add_plane(self.flight_number, self.status, self.position_x, self.position_y, self.position_z, self.velocity_x, self.velocity_y, self.velocity_z)

        if result['msg'] == 'plane crashed':
            self.db.change_status(self.flight_number, result['status'])

        return result


    def control_tower_system(self):
        control_tower = ControlTower(self.dictionary, self.db)
        result = control_tower.guidance_system()
        return result