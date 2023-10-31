import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

class Visualization3D:


    def __init__(self, connection):
        self.fig = plt.figure(figsize=[9,9])
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.db = connection
        self.ani = FuncAnimation(self.fig, self.update, frames=range(100))


    def generate_data(self):
        coordinates = self.db.get_coordinates()
        coordinates = np.array(coordinates).T
        x, y, z, flight_number = coordinates
        return x, y, z, flight_number


    def create_rectangle(self, vertices, face_color, edge_color, alpha):
        rectangle_vertices = [vertices[i] for i in [0, 1, 2, 3]]
        rectangle_poly = [rectangle_vertices]
        rectangle = Poly3DCollection(rectangle_poly, facecolors=face_color, edgecolors=edge_color, alpha=alpha)
        self.ax.add_collection3d(rectangle)


    def update(self, frame):
        self.ax.cla()

        rectangle1_vertices = [(1000, -1025, 0), (1000, -975, 0), (-2500, -975, 0), (-2500, -1025, 0)]
        rectangle2_vertices = [(-1000, 975, 0), (-1000, 1025, 0), (2500, 1025, 0), (2500, 975, 0)]

        self.create_rectangle(rectangle1_vertices, face_color='c', edge_color='b', alpha=0.8)
        self.create_rectangle(rectangle2_vertices, face_color='c', edge_color='r', alpha=0.8)

        x, y, z, flight_number = self.generate_data()

        self.ax.set_xlim(-5500, 5500)
        self.ax.set_ylim(-5500, 5500)
        self.ax.set_zlim(0, 5500)

        self.ax.scatter(x, y, z, c='b', marker='.')

        self.ax.set_xlabel('Oś X')
        self.ax.set_ylabel('Oś Y')
        self.ax.set_zlabel('Oś Z')

        for i, txt in enumerate(flight_number):
            self.ax.text(x[i], y[i], z[i], txt, fontsize=8, color='black')


    def run(self):
        plt.show()
