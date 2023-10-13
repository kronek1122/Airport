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
        result = self.db.add_plane(self.flight_number,'IN_AIR',self.position_x, self.position_y, self.position_z, self.velocity)
        return result
    
    