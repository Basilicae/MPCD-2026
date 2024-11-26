import numpy as np
import matplotlib.pyplot as plt
import scipy.signal.windows
from scipy.signal import stft

iq_path = "C:\Applis\PyCharm\Projects\MDCP\Data\exp1_22.10.24SansDronecentre2.7GHz.iq" #A modifier
iq_path_ad = "C:\Applis\PyCharm\Projects\MDCP\Data\exp2_22.10.24AvecDronecentre2.7GHz.iq"

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

# Affichage du signal IQ dans le domaine temporel
plt.figure(figsize=(12, 6))
plt.plot(I[:1000], label='I')  # On affiche un échantillon des premiers points pour une meilleure visibilité
plt.plot(Q[:1000], label='Q')
plt.plot(I_ad[:1000], label='I_ad')
plt.plot(Q_ad[:1000], label='Q_ad')
plt.xlabel("Echantillons")
plt.ylabel("Amplitude")
plt.title("Signal IQ dans le Domaine Temporel")
plt.legend()
plt.show()

# Calcul et affichage de la Transformée de Fourier
spectrum = np.fft.fftshift(np.fft.fft(IQ_complex))
freq = np.fft.fftshift(np.fft.fftfreq(len(IQ_complex), d=1/sample_rate))
spectrum_ad = np.fft.fftshift(np.fft.fft(IQ_complex_ad))
freq_ad = np.fft.fftshift(np.fft.fftfreq(len(IQ_complex_ad), d=1/sample_rate))

# Affichage du spectre de puissance en dB
plt.figure(figsize=(12, 6))
plt.plot(freq, 20 * np.log10(np.abs(spectrum)))
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude (dB)")
plt.title("Spectre de Puissance du Signal IQ")
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(freq_ad, 20 * np.log10(np.abs(spectrum_ad)))
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude (dB)")
plt.title("Spectre de Puissance du Signal IQ_ad")
plt.show()


nperseg = 2048  # nombre de points par segment (à ajuster pour la résolution souhaitée)
noverlap = nperseg // 2  # nombre de points de chevauchement (50% ici)
window = "barthann"
frequences, temps, spectrogramme = stft(IQ_complex, noverlap = noverlap, nperseg=nperseg, return_onesided=False, fs=sample_rate,window=window)
plt.figure(figsize=(12, 6))
plt.pcolormesh(temps, frequences, 10*np.log10(np.abs(spectrogramme)+1e-6), shading='gouraud')
plt.colorbar(label='Amplitude')
plt.ylabel("Fréquence (Hz)")
plt.xlabel("Temps (s)")
plt.title("STFT (Spectrogramme) du signal IQ")
plt.show()

nperseg = 2048  # nombre de points par segment (à ajuster pour la résolution souhaitée)
noverlap = nperseg // 2  # nombre de points de chevauchement (50% ici)
window = "barthann"
frequences_ad, temps_ad, spectrogramme_ad = stft(IQ_complex_ad, noverlap = noverlap, nperseg=nperseg, return_onesided=False, fs=sample_rate, window=window)
plt.figure(figsize=(12, 6))
plt.pcolormesh(temps, frequences_ad, 10*np.log10(np.abs(spectrogramme_ad)+1e-6), shading='gouraud')
plt.colorbar(label='Amplitude')
plt.ylabel("Fréquence (Hz)")
plt.xlabel("Temps (s)")
plt.title("STFT (Spectrogramme) du signal IQ_ad")
plt.show()