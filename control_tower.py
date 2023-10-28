
class ControlTower:
    SECTOR_A = (-2000, 1750, 500)
    SECTOR_B = (-2000, 1000, 400)
    SECTOR_C = (-1000, 1000, 100)
    SECTOR_D = (2000, -1750, 500)
    SECTOR_E = (2000, -1000, 400)
    SECTOR_F = (1000, -1000, 100)
    SECTOR_R1 = (1500, 1000, 0)
    SECTOR_R2 = (-1500, -1000, 0)

    def __init__(self, dictionary:dict):
        self.position_x = dictionary['position_x']
        self.position_y = dictionary['position_y']
        self.position_z = dictionary['position_z']
        self.velocity = dictionary['velocity_vector']
        self.velocity_x = self.velocity[0]
        self.velocity_y = self.velocity[1]
        self.velocity_z = self.velocity[2]
        print(dictionary)


    def guidance_system(self):
        if self.position_x >= -2500 and self.position_y >= 2000:
            print('sektor A')
            vector = self.vector_calculation(self.SECTOR_A,(self.position_x, self.position_y, self.position_z))

        elif self.position_x <= 2500 and self.position_y <= -2000:
            print('sektor D')
            vector = self.vector_calculation(self.SECTOR_D,(self.position_x, self.position_y, self.position_z))

        elif self.position_x < -2500 and self.position_y > -2000:
            print('sektor B')
            vector = self.vector_calculation(self.SECTOR_B,(self.position_x, self.position_y, self.position_z))
        
        elif self.position_x > 2500 and self.position_y < 2000:
            print('sektor E')
            vector = self.vector_calculation(self.SECTOR_E,(self.position_x, self.position_y, self.position_z))

        elif self.position_x < -1500 and self.position_y > 0:
            print('sektor AB')
            vector = self.vector_calculation(self.SECTOR_C,(self.position_x, self.position_y, self.position_z))

        elif self.position_x > 1500 and self.position_y < 0:
            print('sektor ED')
            vector = self.vector_calculation(self.SECTOR_F,(self.position_x, self.position_y, self.position_z))

        elif self.position_x < -1000 and self.position_y > 0:
            print('sektor C')
            vector = self.vector_calculation(self.SECTOR_R1,(self.position_x, self.position_y, self.position_z))

        elif self.position_x > 1000 and self.position_y < 0:
            print('sektor F')
            vector = self.vector_calculation(self.SECTOR_R2,(self.position_x, self.position_y, self.position_z))

        elif self.position_x > 800 and self.position_y > 0:
            print('sektor L1')
            vector = self.vector_calculation(self.SECTOR_R1,(self.position_x, self.position_y, self.position_z))

        elif self.position_x < -800 and self.position_y < 0:
            print('sektor L2')
            vector = self.vector_calculation(self.SECTOR_R2,(self.position_x, self.position_y, self.position_z))

        else:
            vector = self.dictionary_data_pack()
        return vector

    def dictionary_data_pack(self):
        result = {'msg':'change direction',
                  'status':"IN_AIR",
                  'velocity_vector':self.velocity}
        print(f'wektor: {self.velocity}')
        return result
    

    def vector_calculation(self, point_one:tuple ,point_two:tuple)->float:
        vector_x_change = point_one[0] - point_two[0]
        vector_y_change = point_one[1] - point_two[1]
        vector_z_change = point_one[2] - point_two[2]

        distance = (vector_x_change**2 + vector_y_change**2 + vector_z_change**2)**0.5
        self.vector_change_adjustment(vector_x_change, vector_y_change, vector_z_change, self.calc_time_at_const_speed(distance))
        print(f'dystans: {distance}')
        result = self.dictionary_data_pack()
        return result
    

    def calc_time_at_const_speed(self, distance:float)->float:
        result = (distance / 250)
        print(f'czas: {result}')
        return result


    def vector_change_adjustment(self, x:float, y:float, z:float, time:float):
        self.velocity[0] = round(x / time)
        self.velocity[1] = round(y / time)
        self.velocity[2] = round(z / time)
        print(f'składowe wektora{self.velocity}')








