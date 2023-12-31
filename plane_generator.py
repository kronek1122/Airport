import random as r


class PlaneGenerator:

    def __init__(self):
        self.direction = r.choice(['NNE','ENE','NNW','WNW','SSE','ESE','SSW','WSW'])
        self.velocity = r.randint(200,300)

    def position_generator(self):
        match self.direction:
            case'NNE':
                position = [r.randint(0,5000), r.randint(4500,5000), r.randint(2000,5000)]
            case'ENE':
                position = [r.randint(4500,5000), r.randint(0,5000), r.randint(2000,5000)]
            case'NNW':
                position = [-r.randint(0,5000), r.randint(4500,5000), r.randint(2000,5000)]
            case'WNW':
                position = [-r.randint(4500,5000), r.randint(0,5000), r.randint(2000,5000)]
            case'SSE':
                position = [r.randint(0,5000), -r.randint(4500,5000), r.randint(2000,5000)]
            case'ESE':
                position = [r.randint(4500,5000), -r.randint(0,5000), r.randint(2000,5000)]
            case'SSW':
                position = [-r.randint(0,5000), -r.randint(4500,5000), r.randint(2000,5000)]
            case'WSW':
                position = [-r.randint(4500,5000), -r.randint(0,5000), r.randint(2000,5000)]
        return position

    def vector_generator(self):
        self.velocity_vector_x = r.randint(0,self.velocity)
        match self.direction:
            case'NNE' | 'ENE':
                vector = [-self.velocity_vector_x, -int((self.velocity**2-self.velocity_vector_x**2)**0.5), 0]
            case'NNW' | 'WNW':
                vector = [self.velocity_vector_x, -int((self.velocity**2-self.velocity_vector_x**2)**0.5), 0]
            case'SSE' | 'ESE':
                vector = [-self.velocity_vector_x, int((self.velocity**2-self.velocity_vector_x**2)**0.5), 0]
            case'SSW' | 'WSW':
                vector = [self.velocity_vector_x, int((self.velocity**2-self.velocity_vector_x**2)**0.5), 0]
        return vector


