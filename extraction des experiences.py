import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft

### Extraction fichier : On obtient une liste de [I,Q,I,Q...]

# 1e étape : Déf de la fct lecture de fichier
def read_iq_file(file_path, data_type=np.int16):
    iq_data = np.fromfile(file_path, dtype=data_type)  # Lire le fichier binaire
    return iq_data

# 2e étape : Comparaison des mesures avec ou sans drone
file_path_1 = "C:\Applis\PyCharm\Projects\MDCP\Data\exp1_22.10.24SansDronecentre2.7GHz.iq"
sd = read_iq_file(file_path_1)
file_path_2 = "C:\Applis\PyCharm\Projects\MDCP\Data\exp2_22.10.24AvecDronecentre2.7GHz.iq"
ad = read_iq_file(file_path_2)



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
    return np.array(pairs), np.array(impairs)

Isd, Qsd = separer_indices(sd)
Iad, Qad = separer_indices(ad)

# 2e étape : Reconstitution du signal
def x(I, Q):
    return I + 1j * Q               #(I * np.cos(2 * np.pi * f * t) + Q * np.sin(2 * np.pi * f * t))
#a = x(Isd, Qsd)

# # 3e étape : Tracé des signaux
# t = np.linspace(0, len(sd) + 1, 2000000)
# plt.plot(t, x(Isd, Qsd), label="xsd")
# plt.plot(t, x(Iad, Qad), label="xad")
# #plt.plot(t, x(t, Idelta, Qdelta, 2.7e9), label="xdelta")
# plt.legend()
# plt.xlabel('t')
# plt.ylabel('Données')
# plt.title('Tracé des signaux')
# plt.grid(True)
# plt.show()



### Transformées

# 1e étape : TF(x) et STFT (X)
def STFT(signal):
    return stft(signal, fs=5e-9)

fsd, Tsd, Zxxsd = STFT(x(Isd, Qsd))
fad, Tad, Zxxad = STFT(x(Iad, Qad))

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

# # Calcul et tracé des Transformées de Fourier
# Xsd = np.fft.fft(x(Isd, Qsd))
# Xad = np.fft.fft(x(Iad, Qad))
#
# fe = 2e+08
# freqs = np.fft.fftfreq(len(Xsd), d=1/fe)
#
# plt.plot(freqs, np.abs(Xsd), label="Xsd")
# plt.plot(freqs, np.abs(Xad), label="Xad")
# plt.xlabel("Frequency (Hz)")
# plt.ylabel("Amplitude")
# plt.title("Fourier Transform of Reconstructed Signals")
# plt.legend()
# plt.show()