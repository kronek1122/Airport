'''Manage planes script'''

import os
from dotenv import load_dotenv
from plane_generator import PlaneGenerator
from db_manager import DatabaseManager

load_dotenv()


class PlaneManager:
    
    def __init__(self):
        postgres_config_str = os.getenv('POSTGRES_CONFIG')
        self.postgres_config = eval(postgres_config_str)
        self.flight_number = PlaneGenerator().flight_number_generator()
        self.position = PlaneGenerator().position_generator()
        self.position_x = self.position[0]
        self.position_y = self.position[1]
        self.position_z = self.position[2]
        self.velocity = PlaneGenerator().vector_generator()
        self.db = DatabaseManager(**self.postgres_config)

    def new_plane(self):
        result = self.db.add_plane(next(self.flight_number),'IN_AIR',self.position_x, self.position_y, self.position_z, self.velocity)
        return result
    
    