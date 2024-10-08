import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft
from points import objet_translation, objet_rotation, objet_vibration  # Assurez-vous que le nom du fichier est correct

# Fonction pour simuler le signal de retour radar
def simuler_retour_radar(objet, nombre_etapes_temps, longueur_onde_radar, frequence_echantillonnage):
    """
    Simule le signal de retour radar d'un objet drone en mouvement.
    :param objet: L'objet drone avec des points en mouvement
    :param nombre_etapes_temps: Nombre d'étapes de temps pour la simulation
    :param longueur_onde_radar: Longueur d'onde du signal radar
    :param frequence_echantillonnage: Fréquence d'échantillonnage
    :return: Le signal radar simulé dans le temps
    """
    signal_radar = np.zeros(nombre_etapes_temps)
    delta_t = 1 / frequence_echantillonnage
    for t in range(nombre_etapes_temps):
        objet.calc_points(t * delta_t)  #position de l'objet
        vitesse_relative = objet.vitesse(t * delta_t, delta_t)
        decallage_doppler = (2 * vitesse_relative) / longueur_onde_radar
        signal_radar[t] = np.sum(np.cos(2 * np.pi * decallage_doppler))
    return signal_radar


def generer_spectrogramme(signal_radar, frequence_echantillonnage, titre):
    """
    Génère et trace le spectrogramme du signal radar.
    :param signal_radar: Le signal de retour radar
    :param frequence_echantillonnage: Fréquence d'échantillonnage
    :param titre: Titre pour le tracé du spectrogramme
    """
    f, t, Zxx = stft(signal_radar, fs=frequence_echantillonnage, nperseg=256)  # Transformée de Fourier à court terme
    plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
    plt.title(titre)
    plt.ylabel('Fréquence [Hz]')
    plt.xlabel('Temps [sec]')
    plt.colorbar(label='Amplitude')
    plt.ylim(0, 20)  #à ajuster
    plt.show()


# Exemple d'utilisation
if __name__ == '__main__':
    longueur_onde_radar = 0.03
    frequence_echantillonnage = 1000
    nombre_etapes_temps = 10000

    # Définir les points initiaux(ex: des points de rotor)
    points_init = [[1, 1, 0],
                   [-1, 1, 0],
                   [-1, -1, 0],
                   [1, -1, 0]]

    # Simuler translation, rotation et vibration
    # Translation: Mouvement dans la direction x avec une vitesse de 1 m/s, distance maximale de 10 mètres
    objet_translation_ = objet_translation(1, points_init, (0, 0, 0), d=10, u=(1, 0, 0), v=1, radar=(0, 0, 0))
    signal_radar_translation = simuler_retour_radar(objet_translation_, nombre_etapes_temps, longueur_onde_radar,
                                                    frequence_echantillonnage)
    generer_spectrogramme(signal_radar_translation, frequence_echantillonnage, "Signature Micro-Doppler: Translation")

    # Rotation: Rotation autour de l'axe z à 5 degrés par seconde
    objet_rotation_ = objet_rotation(1, points_init, (0, 0, 0), v=5, u=(0, 0, 1), radar=(0, 0, 0))
    signal_radar_rotation = simuler_retour_radar(objet_rotation_, nombre_etapes_temps, longueur_onde_radar,
                                                 frequence_echantillonnage)
    generer_spectrogramme(signal_radar_rotation, frequence_echantillonnage, "Signature Micro-Doppler: Rotation")

    # Vibration: Vibration le long de l'axe x avec une amplitude de 3, vitesse de 0.2
    objet_vibration_ = objet_vibration(1, points_init, (0, 0, 0), d=3, u=(1, 0, 0), v=0.2, radar=(0, 0, 0))
    signal_radar_vibration = simuler_retour_radar(objet_vibration_, nombre_etapes_temps, longueur_onde_radar,
                                                  frequence_echantillonnage)
    generer_spectrogramme(signal_radar_vibration, frequence_echantillonnage, "Signature Micro-Doppler: Vibration")

