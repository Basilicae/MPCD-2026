import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft
from points import objet_translation, objet_rotation, objet_vibration, objet_fixe, affiche_scene  # Assurez-vous que le nom du fichier est correct
from PIL import Image


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
    delta_t = 1 / frequence_echantillonnage  # Incrément de temps entre les échantillons
    for t in range(nombre_etapes_temps):
        objet.calc_points(t * delta_t)  # Mettre à jour la position de l'objet
        # Calculer la vitesse relative de chaque point
        vitesse_relative = objet.vitesse(t * delta_t, delta_t)
        # Calculer le décalage Doppler pour chaque point
        decallage_doppler = (2 * vitesse_relative) / longueur_onde_radar
        # Somme des retours radar (signaux cosinus) de tous les points
        signal_radar[t] = np.sum(np.cos(2 * np.pi * decallage_doppler)) #Pourquoi cos ?
    return signal_radar

c = 3E8 #m/s
def spectrogramme(lambda_, scene, tps_exp, f_e, bornes_f = None,res_f = 600):
    if bornes_f == None:
        bornes_f = (- 2 * 80 / lambda_, 2 * 80 / lambda_) #En l'abscence de bornes, on considère que la vitesse max relative au radar est de 80m/s
    nb_tps = int(tps_exp * f_e)
    valeurs = np.zeros((res_f, nb_tps))
    for i in range(nb_tps):
        for obj in scene:
            for v in obj.vitesse(i/f_e, 1/f_e):
                ind = 2*v/lambda_ - bornes_f[0]
                frequ_aff = int(ind * res_f / (bornes_f[1]-bornes_f[0]))
                if 0 <= frequ_aff < res_f: #Si notre fenètre permet d'afficher la fréquence
                    valeurs[frequ_aff, i] += obj.coeff
                else:
                    print("wowowow")
    #On normalise pour afficher
    valeurs = np.uint8(valeurs * 255 / np.max(valeurs))
    img = Image.fromarray(valeurs)
    return img



# Fonction pour générer et tracer le spectrogramme (représentation temps-fréquence)
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
    plt.ylim(0, 20)  # Limiter la plage de fréquence pour la clarté; ajuster si nécessaire
    plt.show()


# Exemple d'utilisation
if __name__ == '__main__nope':
    # Paramètres de simulation radar
    longueur_onde_radar = 0.03  # Longueur d'onde de 3 cm
    frequence_echantillonnage = 1000  # Fréquence d'échantillonnage augmentée (2000 Hz)
    nombre_etapes_temps = 10000  # Nombre d'étapes de temps pour la simulation

    # Définir les points initiaux pour le drone (ex: un carré ou des points de rotor)

    points_init = [[1, 1, 0],
                   [-1, 1, 0],
                   [-1, -1, 0],
                   [1, -1, 0]]

    # Simuler translation, rotation et vibration
    # Translation: Mouvement dans la direction x avec une vitesse de 1 m/s, distance maximale de 10 mètres
    objet_translation_ = objet_translation(1, points_init, (0, 0, 0), d=10, u=(1, 0, 0), v=1, radar=(0, 0, 0))

    # Rotation: Rotation autour de l'axe z à 5 radians par seconde
    objet_rotation_ = objet_rotation(1, points_init, (0, 0, 0), v=5              , u=(0, 0, 1), radar=(0, 0, 0))

    # Vibration: Vibration le long de l'axe x avec une amplitude de 3, vitesse de 0.2
    objet_vibration_ = objet_vibration(1, points_init, (0, 0, 0), d=3, u=(1, 0, 0), v=0.2, radar=(0, 0, 0))

    spectrogramme(3e-2, [objet_rotation_], 0.1, 100000)
    # Simuler le signal radar pour la translation
    signal_radar_translation = simuler_retour_radar(objet_translation_, nombre_etapes_temps, longueur_onde_radar, frequence_echantillonnage)
    generer_spectrogramme(signal_radar_translation, frequence_echantillonnage, "Signature Micro-Doppler: Translation")

    # Simuler le signal radar pour la rotation
    signal_radar_rotation = simuler_retour_radar(objet_rotation_, nombre_etapes_temps, longueur_onde_radar, frequence_echantillonnage)
    generer_spectrogramme(signal_radar_rotation, frequence_echantillonnage, "Signature Micro-Doppler: Rotation")

    # Simuler le signal radar pour la vibration
    signal_radar_vibration = simuler_retour_radar(objet_vibration_, nombre_etapes_temps, longueur_onde_radar, frequence_echantillonnage)
    generer_spectrogramme(signal_radar_vibration, frequence_echantillonnage, "Signature Micro-Doppler: Vibration")

if __name__ == "__main__":
    demonstration = "rotation_helice-4pt"
    if demonstration == "rotation_simple":
        points_init = [[1,1,0]]
        print(objet_rotation)
        objet_rotation_ = objet_rotation(1, points_init, (0, 0, 0), v=20, u=(0, 0, 1), radar=(-10, 0, 0))
        battie = objet_fixe(1, [[0,0,0]], (-10,0,0))
        #affiche_scene([objet_rotation_, battie], 100, 5)
        img = spectrogramme(3E-2, [objet_rotation_, battie],0.5,300,bornes_f=(-6000,6000))
        img.save("premiere_exp_fe_dim.png")
    elif demonstration == "rotation_helice-4pt":
        points_init = [[1,1,0], [-1,1,0],[0,-np.sqrt(2),0]]
        objet_rotation_ = objet_rotation(3, points_init, (0, 0, 0), v=20, u=(0, 0, 1), radar=(-10, 0, 0))
        battie = objet_fixe(1, [[0, 0, 0]], (-10, 0, 0))
        img = spectrogramme(3E-2, [objet_rotation_, battie],3,300,bornes_f=(-6000,6000))
        img.save("premiere_exp_fe_dim.png")
    elif demonstration == "une troisième demo wowowow":
        print('salut')