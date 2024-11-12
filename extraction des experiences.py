import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft

### Extraction fichier : On obtient une liste de [I,Q,I,Q...]

# 1e étape : Déf de la fct lecture de fichier
def read_iq_file(file_path, data_type=np.float32):
    iq_data = np.fromfile(file_path, dtype=data_type)  # Lire le fichier binaire
    return iq_data

# 2e étape : Comparaison des mesures avec ou sans drone
file_path_1 = "C:\Applis\PyCharm\Projects\MDCP\Data\exp1_22.10.24SansDronecentre2.7GHz.iq"
sd = read_iq_file(file_path_1)
file_path_2 = "C:\Applis\PyCharm\Projects\MDCP\Data\exp2_22.10.24AvecDronecentre2.7GHz.iq"
ad = read_iq_file(file_path_2)
delta = ad - sd

### Reconstitution du signal

# 1e étape : Séparation des indices pour obtenir I et Q
def separer_indices(liste):
    pairs = []
    impairs = []
    for i in range(len(liste)):
        if i % 2 == 0:
            pairs.append(liste[i])
        else:
            impairs.append(liste[i])
    return pairs, impairs

Isd, Qsd = separer_indices(sd)
Iad, Qad = separer_indices(ad)
Idelta, Qdelta = separer_indices(delta)

# Remplacement des valeurs NaN par 0 dans les composants I et Q
Isd = np.nan_to_num(Isd, nan=0.0)
Qsd = np.nan_to_num(Qsd, nan=0.0)
Iad = np.nan_to_num(Iad, nan=0.0)
Qad = np.nan_to_num(Qad, nan=0.0)
Idelta = np.nan_to_num(Idelta, nan=0.0)
Qdelta = np.nan_to_num(Qdelta, nan=0.0)

# 2e étape : Reconstitution du signal
def x(t, I, Q, f):
    return I * np.cos(2 * np.pi * f * t) + Q * np.sin(2 * np.pi * f * t)

# 3e étape : Tracé des signaux
t = np.linspace(0, len(sd) + 1, 1000000)
plt.plot(t, x(t, Isd, Qsd, 2.7e9), label="xsd")
plt.plot(t, x(t, Iad, Qad, 2.7e9), label="xad")
#plt.plot(t, x(t, Idelta, Qdelta, 2.7e9), label="xdelta")
plt.legend()
plt.xlabel('t')
plt.ylabel('Données')
plt.title('Tracé des signaux')
plt.grid(True)
plt.show()

### Transformées

# 1e étape : TF(x) et STFT (X)
def STFT(signal):
    return stft(signal, fs=5e-9)

fsd, Tsd, Zxxsd = STFT(x(t, Isd, Qsd, 2.7e9))
fad, Tad, Zxxad = STFT(x(t, Iad, Qad, 2.7e9))

# Affichage des spectrogrammes STFT
plt.figure()
plt.pcolormesh(Tsd, fsd, 10 * np.log10(np.abs(Zxxsd)))
plt.title("STFT - Experiment 1 (No Drone)")
plt.colorbar(label="Magnitude (dB)")
plt.show()

plt.figure()
plt.pcolormesh(Tad, fad, 10 * np.log10(np.abs(Zxxad)))
plt.title("STFT - Experiment 2 (With Drone)")
plt.colorbar(label="Magnitude (dB)")
plt.show()

# Calcul et tracé des Transformées de Fourier
Xsd = np.fft.fft(x(t, Isd, Qsd, 2.7e9))
Xad = np.fft.fft(x(t, Iad, Qad, 2.7e9))

fe = 1
freqs = np.fft.fftfreq(len(Xsd), d=1/fe)

plt.plot(freqs, np.abs(Xsd), label="Xsd")
plt.plot(freqs, np.abs(Xad), label="Xad")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.title("Fourier Transform of Reconstructed Signals")
plt.legend()
plt.show()