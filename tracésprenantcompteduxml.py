import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft

iq_path = "C:\Applis\PyCharm\Projects\MDCP\Data\exp1_22.10.24SansDronecentre2.7GHz.iq" #A modifier



# Extraction des paramètres à partir des métadonnées
sample_rate = 2e8
scale_factor = 10



iq_data = np.fromfile(iq_path, dtype=np.int16)

# Conversion des données en I et Q et application du facteur d'échelle
I = iq_data[::2] * scale_factor  # Composante I
Q = iq_data[1::2] * scale_factor  # Composante Q

# Conversion en format complexe pour la Transformée de Fourier
IQ_complex = I + 1j * Q

# Affichage du signal IQ dans le domaine temporel
plt.figure(figsize=(12, 6))
plt.plot(I[:1000], label='I')  # On affiche un échantillon des premiers points pour une meilleure visibilité
plt.plot(Q[:1000], label='Q')
plt.xlabel("Echantillons")
plt.ylabel("Amplitude")
plt.title("Signal IQ dans le Domaine Temporel")
plt.legend()
plt.show()

# Calcul et affichage de la Transformée de Fourier
spectrum = np.fft.fftshift(np.fft.fft(IQ_complex))
freq = np.fft.fftshift(np.fft.fftfreq(len(IQ_complex), d=1/sample_rate))

# Affichage du spectre de puissance en dB
plt.figure(figsize=(12, 6))
plt.plot(freq, 20 * np.log10(np.abs(spectrum)))
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude (dB)")
plt.title("Spectre de Puissance du Signal IQ")
plt.show()



nperseg = 2048  # nombre de points par segment (à ajuster pour la résolution souhaitée)
noverlap = nperseg // 2  # nombre de points de chevauchement (50% ici)
frequences, temps, spectrogramme = stft(IQ_complex, noverlap = noverlap, nperseg=nperseg, return_onesided=False, fs=sample_rate)
plt.figure(figsize=(12, 6))
plt.pcolormesh(temps, frequences, 10*np.log10(np.abs(spectrogramme)+1e-6), shading='gouraud')
plt.colorbar(label='Amplitude')
plt.ylabel("Fréquence (Hz)")
plt.xlabel("Temps (s)")
plt.title("STFT (Spectrogramme) du signal IQ")
plt.show()