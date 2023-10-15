'''Manage planes script'''

import os
from dotenv import load_dotenv
from db_manager import DatabaseManager

load_dotenv()


class PlaneManager:
    
    def __init__(self, dictionary):
        postgres_config_str = os.getenv('POSTGRES_CONFIG_DB')
        self.postgres_config = eval(postgres_config_str)
        self.flight_number = dictionary['flight_number']
        self.position_x = dictionary['position x']
        self.position_y = dictionary['position y']
        self.position_z = dictionary['position_z']
        self.velocity = dictionary['velocity_vector']
        self.db = DatabaseManager(**self.postgres_config)


    def plane_signal(self):
        if self.position_z == 0:
            self.db.change_status(self.flight_number, 'LANDED')
            msg = f'flight number {self.flight_number} landed'
            print(msg)
            result = 'landed'
        else:
            if self.db.num_of_plane_over_the_airport() < 100:
                msg = self.db.add_plane(self.flight_number,'IN_AIR',self.position_x, self.position_y, self.position_z, self.velocity)
                if msg == 'Error adding new plane to db':
                    self.db.change_velocity_vector(self.flight_number,self.velocity)
                    self.db.mod_plane_position(self.flight_number, self.position_x, self.position_y, self.position_z)
                    result = self.control_tower_system()
                else:
                    result = self.control_tower_system()
            else: 
                result = 'to many planes in the air'
        return result


    def control_tower_system(self):
        #dodać system sterowanie ruchem
        result = self.dictionary_data_pack()
        return result


    def dictionary_data_pack(self):
        result = {'velocity_vector':self.velocity}
        return result

    
    