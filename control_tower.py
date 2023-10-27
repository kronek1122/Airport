
class ControlTower:
    SECTOR_A = (-2499, 1999, 750)
    SECTOR_B = (-2499, 1000, 600)
    SECTOR_C = (-1499, 1000, 200)
    SECTOR_D = (2499, -1999, 750)
    SECTOR_E = (2499, -1000, 600)
    SECTOR_F = (1499, -1000, 200)

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
            distance = self.distance_calculation((self.position_x, self.position_y, self.position_z),self.SECTOR_A)

        elif self.position_x <= 2500 and self.position_y <= -2000:
            distance = self.distance_calculation((self.position_x, self.position_y, self.position_z),self.SECTOR_D)

        elif self.position_x < -2500 and self.position_y > -2000:
            distance = self.distance_calculation((self.position_x, self.position_y, self.position_z),self.SECTOR_B)
        
        elif self.position_x > 2500 and self.position_y < 2000:
            distance = self.distance_calculation((self.position_x, self.position_y, self.position_z),self.SECTOR_E)

        else:
            print("błędne koordynaty")

        self.vector_change_adjustment(self.velocity, self.calc_time_at_const_speed(distance))
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
        return distance
    

    def calc_time_at_const_speed(self, distance:float)->float:
        result = distance / 250
        return result


    def vector_change_adjustment(self, vector:list, time:float):
        self.velocity[0] = round(vector[0] / time)
        self.velocity[1] = round(vector[1] / time)
        self.velocity[2] = round(vector[2] / time)








