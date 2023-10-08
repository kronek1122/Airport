'''Manage planes script'''

from plane_generator import PlaneGenerator
from db_manager import DatabaseManager

class PlaneManager:
    
    def __init__(self):
        self.flight_number = next(PlaneGenerator().flight_number_generator())
        self.position = PlaneGenerator().position_generator()
        self.position_x = self.position[0]
        self.position_y = self.position[1]
        self.position_z = self.position[2]
        self.velocity = PlaneGenerator().vector_generator()


    def new_plane(self):
        result = DatabaseManager().add_plane(self.flight_number,'IN_AIR',self.position_x, self.position_y, self.position_z, self.velocity)
        return result