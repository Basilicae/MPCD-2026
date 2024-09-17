import numpy
import numpy as np


class objet:
    def __init__(self, n):
        self.n = n


class objet_fixe(objet):
    def __init__(self, n,  points):
        super().__init__(n)
        self.points = points

    def calc_points(self, t):
        pass



class objet_rotation(objet):
    def __init__(self, n, points,  centre, v, u):
        """
        :param n: Le nombre de points de l'objet
        :param points: Une liste de tuple de taille 3, chacun représentant les cooedonnées d'un point par rapport au centre
        :param centre: La position du centre de rotation par rapport au centre de l'objet complet
        :param v: La vitesse de rotation en degrées par secondes
        :param u: Le vecteur qui définit le sens de rotation
        """
        super().__init__(n)
        self.points = numpy.array(points)
        self.centre = np.array(centre)
        self.ones = np.ones((1,n))
        self.v, self.u =v, u

    def calcul_rot(self, theta):
        u = self.u
        c = np.cos(theta)
        s = np.sin(theta)
        self.rot = np.array([[u[0]**2*(1-c)+c, u[0]*u[1]*(1-c)-u[2]*s, u[0]*u[2]*(1-c)+u[1]*s],
                             [u[0]*u[1]*(1-c) + u[1]**2*(1-c)+c, u[1]*u[2]*(1-c) - u[0]*s],
                             [u[0]*u[2]*(1-c)-u[1]*s, u[1]*u[2]*(1-c)+u[0]*s, u[2]**2*(1-c)+c]])
    def calc_points(self, t):
        self.calcul_rot(self.v*t)
        self.points = self.centre @ self.ones + self.rot @ self.points

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_3d_points(x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c='r', marker='o')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()




#wsh bien
# Exemple d'utilisation
x = np.array([1, 2, 3, 4, 5])
y = np.array([5, 6, 2, 3, 13])
z = np.array([2, 3, 3, 3, 5])

plot_3d_points(x, y, z)
