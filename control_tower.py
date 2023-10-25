
class ControlTower:

    def __init__(self, dictionary:dict):
        self.position_x = dictionary['position_x']
        self.position_y = dictionary['position_y']
        self.position_z = dictionary['position_z']
        self.velocity = dictionary['velocity_vector']
        self.velocity_x = self.velocity[0]
        self.velocity_y = self.velocity[1]
        self.velocity_z = self.velocity[2]


    def guidance_system(self):
        if self.position_x >= -2500 and self.position_y >= 2000:
            pass
        elif self.position_x <= 2500 and self.position_y <= -2000:
            pass
        elif self.position_x >= -5000 and self.position_y >= -2000:
            pass
        elif self.position_x <= 5000 and self.position_y <= 2000:
            pass
        else:
            print("błędne koordynaty")


    def dictionary_data_pack(self):
        result = {'msg':'change direction',
                  'status':"IN_AIR",
                  'velocity_vector':self.velocity}
        return result