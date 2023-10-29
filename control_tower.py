
class ControlTower:
    SECTOR_A = (-2000, 1750, 500)
    SECTOR_B = (-2000, 1000, 400)
    SECTOR_C = (-1000, 1000, 100)
    SECTOR_D = (2000, -1750, 500)
    SECTOR_E = (2000, -1000, 400)
    SECTOR_F = (1000, -1000, 100)
    SECTOR_R1 = (1000, 1000, 0)
    SECTOR_R2 = (-1000, -1000, 0)

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
            print('sektor A')
            distance = self.distance_calculation(self.SECTOR_A,(self.position_x, self.position_y, self.position_z))
            speed = 250

        elif self.position_x <= 2500 and self.position_y <= -2000:
            print('sektor D')
            distance = self.distance_calculation(self.SECTOR_D,(self.position_x, self.position_y, self.position_z))
            speed = 250

        elif self.position_x < -2500 and self.position_y > -2000:
            print('sektor B')
            distance = self.distance_calculation(self.SECTOR_B,(self.position_x, self.position_y, self.position_z))
            speed = 250

        elif self.position_x > 2500 and self.position_y < 2000:
            print('sektor E')
            distance = self.distance_calculation(self.SECTOR_E,(self.position_x, self.position_y, self.position_z))
            speed = 250

        elif self.position_x < -1500 and self.position_y > 0:
            print('sektor AB')
            distance = self.distance_calculation(self.SECTOR_C,(self.position_x, self.position_y, self.position_z))
            speed = 160

        elif self.position_x > 1500 and self.position_y < 0:
            print('sektor ED')
            distance = self.distance_calculation(self.SECTOR_F,(self.position_x, self.position_y, self.position_z))
            speed = 160

        elif self.position_x < -1000 and self.position_y > 0:
            print('sektor C')
            distance = self.distance_calculation(self.SECTOR_R1,(self.position_x, self.position_y, self.position_z))
            speed = 100

        elif self.position_x > 1000 and self.position_y < 0:
            print('sektor F')
            distance = self.distance_calculation(self.SECTOR_R2,(self.position_x, self.position_y, self.position_z))
            speed = 100

        elif self.position_x > 800 and self.position_y > 0:
            print('sektor L1')
            distance = self.distance_calculation(self.SECTOR_R1,(self.position_x, self.position_y, self.position_z))
            speed = 80

        elif self.position_x < -800 and self.position_y < 0:
            print('sektor L2')
            distance = self.distance_calculation(self.SECTOR_R2,(self.position_x, self.position_y, self.position_z))
            speed = 80

        else:
            pass

        try:
            time = self.calc_time_at_const_speed(distance['distance'],speed)
            self.vector_change_adjustment(distance['x'],distance['y'], distance['z'], time)
            result = self.dictionary_data_pack()
        except UnboundLocalError:
            result = self.dictionary_data_pack()

        return result


    def dictionary_data_pack(self):
        result = {'msg':'change direction',
                  'status':"IN_AIR",
                  'velocity_vector':self.velocity}
        return result
    

    def distance_calculation(self, point_one:tuple ,point_two:tuple)->float:
        vector_x_change = point_one[0] - point_two[0]
        vector_y_change = point_one[1] - point_two[1]
        vector_z_change = point_one[2] - point_two[2]

        distance = (vector_x_change**2 + vector_y_change**2 + vector_z_change**2)**0.5
        result = {'distance':distance,
                  'x': vector_x_change,
                  'y': vector_y_change,
                  'z': vector_z_change}
        return result
    

    def calc_time_at_const_speed(self, distance:float, speed:float)->float:
        result = (distance / speed)
        return result


    def vector_change_adjustment(self, x:float, y:float, z:float, time:float):
        self.velocity[0] = round(x / time)
        self.velocity[1] = round(y / time)

        if z < -16:
            self.velocity[2] = round(z / time)
        else:
            self.velocity[2] = z
        print(f'składowe wektora{self.velocity}')