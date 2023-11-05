import random


class ControlTower:
    SECTOR_A = (4000, -4000, 1500)
    SECTOR_B = (-3000, -4000, 1500)
    SECTOR_C = (-4000, 4000, 1200)
    SECTOR_D = (3000, 4000, 1200)
    SECTOR_E = (-3000, -2250, 1000)
    SECTOR_F = (3000, 2250, 1000)
    SECTOR_G = (3000, -2500, 750)
    SECTOR_H = (-3000, 2500, 750)
    SECTOR_I = (3000, -1000, 500)
    SECTOR_J = (-3000, 1000, 500)
    SECTOR_K = (1000, -1000, 200)
    SECTOR_L = (-1000, 1000, 200)
    SECTOR_R1 = (-1000, -1000, 0)
    SECTOR_R2 = (1000, 1000, 0)


    def __init__(self, dictionary:dict, connection):
        self.position_x = dictionary['position_x']
        self.position_y = dictionary['position_y']
        self.position_z = dictionary['position_z']
        self.flight_number = dictionary['flight_number']
        self.status = dictionary['status']
        self.velocity = dictionary['velocity_vector']
        self.velocity_x = self.velocity[0]
        self.velocity_y = self.velocity[1]
        self.velocity_z = self.velocity[2]
        self.conn = connection
        self.msg = 'Change direction'


    def guidance_system(self):
        if self.position_x >= 3500 and self.position_y >= -3000:
            distance = self.distance_calculation(self.SECTOR_A,(self.position_x, self.position_y, self.position_z))
            speed = 180

        elif self.position_y < -3000 and self.position_x > -2500:
            distance = self.distance_calculation(self.SECTOR_B,(self.position_x, self.position_y, self.position_z))
            speed = 180

        elif self.position_x < -3500 and self.position_y < 3000:
            distance = self.distance_calculation(self.SECTOR_C,(self.position_x, self.position_y, self.position_z))
            speed = 180

        elif self.position_y > 3000 and self.position_x < 2500:
            distance = self.distance_calculation(self.SECTOR_D,(self.position_x, self.position_y, self.position_z))
            speed = 180

        elif self.position_x < -2500 and self.position_y < -3000:
            distance = self.distance_calculation(self.SECTOR_E,(self.position_x, self.position_y, self.position_z))
            speed = 180

        elif self.position_x > 2500 and self.position_y > 3000:
            distance = self.distance_calculation(self.SECTOR_F,(self.position_x, self.position_y, self.position_z))
            speed = 180

        elif self.position_x < 2500 and self.position_y < -2000:
            distance = self.distance_calculation(self.SECTOR_G,(self.position_x, self.position_y, self.position_z))
            speed = 150

        elif self.position_x > -2500 and self.position_y > 2000:
            distance = self.distance_calculation(self.SECTOR_H,(self.position_x, self.position_y, self.position_z))
            speed = 150

        elif self.position_x > 2500 and self.position_y < -1500:
            distance = self.distance_calculation(self.SECTOR_I,(self.position_x, self.position_y, self.position_z))
            speed = 150

        elif self.position_x < -2500 and self.position_y > 1500:
            distance = self.distance_calculation(self.SECTOR_J,(self.position_x, self.position_y, self.position_z))
            speed = 150

        elif self.position_x > 1500 and self.position_y < -500 and self.position_y > -1500:
            distance = self.distance_calculation(self.SECTOR_K,(self.position_x, self.position_y, self.position_z))
            speed = 120

        elif self.position_x < -1500 and self.position_y > 500 and self.position_y < 1500:
            distance = self.distance_calculation(self.SECTOR_L,(self.position_x, self.position_y, self.position_z))
            speed = 120

        elif self.position_x > 1000 and self.position_y < -850 and self.position_y > 1150:
            distance = self.distance_calculation(self.SECTOR_R1,(self.position_x, self.position_y, self.position_z))
            speed = 110

        elif self.position_x < -1000 and self.position_y > 850 and self.position_y < 1150 :
            distance = self.distance_calculation(self.SECTOR_R2,(self.position_x, self.position_y, self.position_z))
            speed = 110

        else:
            if self.collision_detector(200):
                self.emergency_direction_change()
                if self.collision_detector(20):
                    self.status = 'CRASHED'
                    self.msg = 'plane crashed'

            result = self.dictionary_data_pack()
            return result

        time = self.calc_time_at_const_speed(distance['distance'],speed)
        self.vector_change_adjustment(distance['x'],distance['y'], distance['z'], time)

        if self.collision_detector(200):
            self.emergency_direction_change()
            if self.collision_detector(20):
                self.status = 'CRASHED'
                self.msg = 'plane crashed'

        result = self.dictionary_data_pack()
        return result


    def dictionary_data_pack(self):
        result = {'msg':self.msg,
                  'status':self.status,
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

        if z < -15 or z > 0:
            self.velocity[2] = round(z / time)
        else:
            self.velocity[2] = z
        print(f'składowe wektora{self.velocity}')


    def collision_detector(self, distance):
        x_simul = self.position_x + self.velocity[0]
        y_simul = self.position_y + self.velocity[1]
        z_simul = self.position_z + self.velocity[2]

        coordinates = self.conn.get_coordinates()
        collision_detected = False

        for coord in coordinates:
            x, y, z, flight_num = coord
            if abs(x_simul - x) < distance and abs(y_simul - y) < distance and abs(z_simul - z) < distance and flight_num != self.flight_number:
                collision_detected = True
                break
        
        return collision_detected


    def emergency_direction_change(self):
        point_H1 = (random.randint(-2500,2500),random.randint(2000,4000),random.randint(1000,2000))
        point_H2 = (random.randint(-2500,2500),random.randint(-4000,-2000),random.randint(1000,2000))
        point_H3 = (random.randint(-2500,0),random.randint(2000,3500),random.randint(1000,2000))
        point_H4 = (random.randint(0,2500),random.randint(-3500,-2000),random.randint(1000,2000))

        if self.position_y > 0 and self.position_x > -2500:
            distance = self.distance_calculation(point_H1,(self.position_x, self.position_y, self.position_z))
        
        elif self.position_y < 0 and self.position_x < 2500:
            distance = self.distance_calculation(point_H2,(self.position_x, self.position_y, self.position_z))
        
        elif self.position_y > 0 and self.position_x < -2500:
            distance = self.distance_calculation(point_H3,(self.position_x, self.position_y, self.position_z))
        
        elif self.position_y < 0 and self.position_x > 2500:
            distance = self.distance_calculation(point_H4,(self.position_x, self.position_y, self.position_z))

        time = self.calc_time_at_const_speed(distance['distance'],random.randint(80,200))
        self.vector_change_adjustment(distance['x'],distance['y'], distance['z'], time)
