import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Visualization3D:

    def __init__(self, connection):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.db = connection
        self.ani = FuncAnimation(self.fig, self.update, frames=range(100), interval=60)


    def generate_data(self):
        coordinates = self.db.get_coordinates()
        x = [coord[0] for coord in coordinates]
        y = [coord[1] for coord in coordinates]
        z = [coord[2] for coord in coordinates]
        return x, y, z


    def update(self, frame):
        self.ax.cla()

        x, y, z = self.generate_data()

        self.ax.scatter(x, y, z, c='b', marker='o')

        self.ax.set_xlabel('Oś X')
        self.ax.set_ylabel('Oś Y')
        self.ax.set_zlabel('Oś Z')


    def run(self):
        plt.show()
