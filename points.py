import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

class objet:
    def __init__(self, n, radar):
        self.n = n
        self.radar = radar
    def calc_points(self,  t):
        pass

    def distance_radar(self):
        return np.sqrt(np.sum((self.points - self.radar @ self.ones)**2, axis=1))

    def empl_points(self, num, pas, scatter):
        """
        C'est cette fonction qui est appelé lors de la visualisation.
        :param num: Le numero de la frame a afficher, necessaire au fonctionnement de Funcanimation
        :param pas: Necessaire pour convertir l'incrementation de 1 en 1 en un temps.
        :return: l'emplacement des points de l'objet à l'instant, t = num*pas
        """
        self.calc_points(num*pas)
        scatter._offsets3d = self.centre @ self.ones  + self.points
        return self.points
    def vitesse(self, t, delta_t):
        """
        C'est cette fonction qui est appelé lorsqu'on va vouloir tracer le spectrogramme
        :param
        :param t:
        :param delta_t:
        :return: Un tableau de une ligne et self.n colonnes, chaque colonne indique la vitesse du ième point par rapport au radar
        """
        self.calc_points(t)
        distances = self.distance_radar()
        a = (distances - self.distance_anc)/delta_t
        self.distance_anc = distances
        return a


class objet_fixe(objet):
    def __init__(self, n,  points, radar):
        super().__init__(n, radar)
        self.points = points

    def calc_points(self, t):
        pass

    def vitesse(self, t, delta_t):
        return np.zeros((1,self.n))

class objet_vibration(objet):
    def __init__(self, n, points, centre, d, u, v, radar):
        """

        :param n: Le nombre de points
        :param points: le tableau de points (pas un tab numpy
        :param centre: le centre des points
        :param d:
        :param u:
        :param v:
        """
        super().__init__(n, radar)
        self.points = np.array(points).T
        self.points_init = self.points.copy()
        self.centre = np.atleast_2d(centre).T
        self.d = d
        self.u = np.atleast_2d(u).T
        self.ones = np.ones((1, n))
        self.v = v

    def calc_points(self,  t):
        self.points = (self.u * self.d * np.sin(t*np.pi/2/self.v) )@ self.ones + self.points_init


class objet_translation(objet):
    def __init__(self, n, points, centre, d, u,v,  radar):
        """
        :param n: Nombre de points de l'objet
        :param points: Une liste de tuples, chaque tuple représente un point de l'objet
        :param centre: Le centre de l'objet par rapport à la position initiale
        :param direction: Vecteur directionnel de translation
        :param velocity: Vitesse de translation
        """
        super().__init__(n, radar)
        self.points_init = np.array(points).T
        self.points = self.points_init.copy()
        self.centre = np.atleast_2d(centre).T
        self.d = d
        self.u = np.atleast_2d(u).T
        self.v = v
        self.ones = np.ones((1, n))

    def calc_points(self, t):
        """
        Calcule les points de l'objet en fonction du temps t pour une translation linéaire.
        """
        translation = self.u * (self.d * self.v * t)  # Translation vector over time
        self.points = translation @ self.ones + self.points_init

class objet_rotation(objet):
    def __init__(self, n, points,  centre, v, u, radar):
        """
        :param n: Le nombre de points de l'objet
        :param points: Une liste de tuple de taille 3, chacun représentant les cooedonnées d'un point par rapport au centre
        :param centre: La position du centre de rotation par rapport au centre de l'objet complet
        :param v: La vitesse de rotation en degrées par secondes
        :param u: Le vecteur qui définit le sens de rotation
        """
        super().__init__(n)

        self.radar = np.atleast_2d(radar).T
        self.points_init = np.array(points).T
        print(self.points_init.shape)
        self.points = self.points_init.copy()
        self.centre = np.atleast_2d(centre).T
        self.ones = np.ones((1,n))
        self.v, self.u =v, u
        self.distance_anc = self.distance_radar()
    def calcul_rot(self, theta):
        u = self.u
        c = np.cos(theta)
        s = np.sin(theta)
        self.rot = np.array([[u[0]**2*(1-c)+c, u[0]*u[1]*(1-c)-u[2]*s, u[0]*u[2]*(1-c)+u[1]*s],
                             [u[0]*u[1]*(1-c) + u[2]*s, u[1]**2*(1-c)+c, u[1]*u[2]*(1-c) - u[0]*s],
                             [u[0]*u[2]*(1-c)-u[1]*s, u[1]*u[2]*(1-c)+u[0]*s, u[2]**2*(1-c)+c]])


    def calc_points(self, t):
        self.calcul_rot(self.v*t)
        self.points = self.rot @ self.points_init

class objet_immo(objet):
    def __init__(self, n, points, centre):
        super().init(n)
        self.points = np.array(points).T
        self.ones = np.ones((1,n))
        self.centre = np.atleast_2d(centre).T
        self.vitesse_ = np.zeros((1,n))
    def vitesse(self, t):
        return self.vitesse_




def plot_3d_points(x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(x, y, z, c='r', marker='o')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    def update(num, x, y, z, scatter):
        # Exemple de mouvement : translation des points
        x = x + 0.1 * num
        y = y + 0.1 * num
        z = z + 0.1 * num
        scatter._offsets3d = (x, y, z)
        tab = np.array([x,y,z])
        return x, y, z

    ani = FuncAnimation(fig, update, frames=100, fargs=(x, y, z, scatter), interval=100, blit=False)
    plt.show()

x = np.array([1, 2, 3, 4, 5])
y = np.array([5, 6, 2, 3, 13])
z = np.array([2, 3, 3, 3, 5])

# plot_3d_points(x, y, z)

def affiche_objet(ob : objet, temps_anim, pas):
    frames = int(temps_anim // pas)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(ob.points[:, 0], ob.points[:, 1], ob.points[:, 2], c='r', marker='o')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ani = FuncAnimation(fig, ob.empl_points, frames = frames, fargs=[pas, scatter], interval=pas*1000, blit = False)
    plt.show()

pt_init =           [[1, 1, 0],
                     [-1, 1, 0],
                     [-1, -1, 0],
                     [1, -1, 0]]


rotation = objet_vibration(4, pt_init,(0,0,0), 5, (1,0,0), 0.2, (-15,0,0))

affiche_objet(rotation, 10, 0.1)


def affiche_scene(objets, deplacements, temps_anim, pas):
    """
    Affiche une scène avec plusieurs objets en mouvement.

    :param objets: Liste d'objets à afficher.
    :param deplacements: Liste de fonctions de déplacement correspondantes pour chaque objet.
    :param temps_anim: Durée totale de l'animation en secondes.
    :param pas: Intervalle de temps entre chaque frame de l'animation.
    """
    frames = int(temps_anim // pas)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    scatters = []
    for ob in objets:
        scatter = ax.scatter(ob.points[:, 0], ob.points[:, 1], ob.points[:, 2], marker='o')
        scatters.append(scatter)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    def update(num):
        for i, ob in enumerate(objets):
            ob.calc_points(num * pas)
            scatters[i]._offsets3d = (ob.points[0, :], ob.points[1, :], ob.points[2, :])
        return scatters

    ani = FuncAnimation(fig, update, frames=frames, interval=pas * 1000, blit=False)
    plt.show()

# Exemple d'utilisation
pt_init = [[1, 1, 0], [-1, 1, 0], [-1, -1, 0], [1, -1, 0]]
obj1 = objet_vibration(4, pt_init, (5, 5, 5), 3, (1, 0, 0), 2)
obj2 = objet_rotation(4, pt_init, (0, 0, 0), 5, (0, 0, 1), (10, 10, 10))

affiche_scene([obj1, obj2], [obj1.calc_points, obj2.calc_points], 10, 0.1)