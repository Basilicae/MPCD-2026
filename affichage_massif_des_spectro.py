import numpy as np
import matplotlib.pyplot as plt
import scipy.signal.windows
from scipy.signal import stft

# Utilisation de chaînes brutes pour les chemins de fichiers
iq_path = r"C:\Applis\PyCharm\Projects\MDCP\Data\exp1_22.10.24SansDronecentre2.7GHz.iq"
iq_path_ad = r"C:\Applis\PyCharm\Projects\MDCP\Data\exp2_22.10.24AvecDronecentre2.7GHz.iq"

# Extraction des paramètres à partir des métadonnées
sample_rate = 2e8
scale_factor = 10

iq_data = np.fromfile(iq_path, dtype=np.int16)
iq_data_ad = np.fromfile(iq_path_ad, dtype=np.int16)

# Conversion des données en I et Q et application du facteur d'échelle
I = iq_data[::2] * scale_factor  # Composante I
Q = iq_data[1::2] * scale_factor  # Composante Q

I_ad = iq_data_ad[::2] * scale_factor  # Composante I
Q_ad = iq_data_ad[1::2] * scale_factor  # Composante Q

# Conversion en format complexe pour la Transformée de Fourier
IQ_complex = I + 1j * Q
IQ_complex_ad = I_ad + 1j * Q_ad

import scipy.signal

# Dictionnaire des fenêtres avec leurs paramètres par défaut
fenetres = {
    'boxcar': {},
    'triang': {},
    'blackman': {},
    'hamming': {},
    'hann': {},
    'bartlett': {},
    'flattop': {},
    'parzen': {},
    'bohman': {},
    'blackmanharris': {},
    'nuttall': {},
    'barthann': {},
    'kaiser': {'beta': 14},
    'gaussian': {'std': 0.4},
    'general_gaussian': {'p': 1.5, 'sig': 0.4},
    'dpss': {'NW': 4},
    'chebwin': {'at': 100},
    'exponential': {'tau': 3.0},
    'tukey': {'alpha': 0.5}
}

# Exemple d'utilisation
nperseg = 2048  # nombre de points par segment (à ajuster pour la résolution souhaitée)
noverlap = nperseg // 2  # nombre de points de chevauchement (50% ici)

for fenetre, params in fenetres.items():
    print(f"Fenêtre: {fenetre}, Paramètres: {params}")
    window = scipy.signal.get_window((fenetre, *params.values()), nperseg)
    print(window)

    frequences, temps, spectrogramme = stft(IQ_complex, noverlap=noverlap, nperseg=nperseg, return_onesided=False, fs=sample_rate, window=window)
    plt.figure(figsize=(12, 6))
    plt.pcolormesh(temps, frequences, 10*np.log10(np.abs(spectrogramme)+1e-6), shading='gouraud')
    plt.colorbar(label='Amplitude')
    plt.ylabel("Fréquence (Hz)")
    plt.xlabel("Temps (s)")
    plt.title(f"STFT (Spectrogramme) du signal IQ avec fenêtre {fenetre}")
    plt.show()

    frequences_ad, temps_ad, spectrogramme_ad = stft(IQ_complex_ad, noverlap=noverlap, nperseg=nperseg, return_onesided=False, fs=sample_rate, window=window)
    plt.figure(figsize=(12, 6))
    plt.pcolormesh(temps_ad, frequences_ad, 10*np.log10(np.abs(spectrogramme_ad)+1e-6), shading='gouraud')
    plt.colorbar(label='Amplitude')
    plt.ylabel("Fréquence (Hz)")
    plt.xlabel("Temps (s)")
    plt.title(f"STFT (Spectrogramme) du signal IQ_ad avec fenêtre {fenetre}")
    plt.show()