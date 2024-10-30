import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft

### Extraction fichier : On obtient une liste de [I,Q,I,Q...]

# 1e étape : Déf de la fct lecture de fichier
def read_iq_file(file_path, data_type=np.float32):
    iq_data = np.fromfile(file_path, dtype=data_type) # Lire le fichier binaire
    return iq_data


# 2e étape : Comparaison des mesures avec ou sans drone
file_path_1 = "C:\Applis\PyCharm\Projects\MDCP\Data\exp1_22.10.24SansDronecentre2.7GHz.iq"
sd = read_iq_file(file_path_1)
file_path_2 = "C:\Applis\PyCharm\Projects\MDCP\Data\exp2_22.10.24AvecDronecentre2.7GHz.iq"
ad = read_iq_file(file_path_2)
#delta = ad-sd


# # 3e étape : Tracé des données
# t = np.linspace(0, len(sd)+1, 2000000)
# plt.plot(t, sd, label = "sd")
# plt.plot(t, ad, label = "ad")
# plt.plot(t, delta, label = "delta")
# plt.legend()
# plt.xlabel('t')
# plt.ylabel('Données')
# plt.title('Tracé des données du fichier')
# plt.grid(True)
# plt.show()



### Reconstitution du signal

# 1e étape : récuperer les I et les Q pour reconstituer x(t) = Icos(2pift)  + Qsin(2pift)
def separer_indices(liste):
    pairs = []
    impairs = []
    for i in range(len(liste)):
        if i % 2 == 0:
            pairs.append(liste[i])
        else:
            impairs.append(liste[i])
    return pairs, impairs

Isd,Qsd = separer_indices(sd)
Iad,Qad = separer_indices(ad)
Idelta,Qdelta = separer_indices(delta)

# 2e étape :  reconstituer le signal
def x(t, I, Q, f):
    return I * np.cos(2*np.pi*f*t) + Q * np.sin(2*np.pi*f*t)

# # 3e étape : tracer les signaux
# t = np.linspace(0, len(sd)+1, 1000000)
# plt.plot(t, x(t,Isd,Qsd,2.7e9), label = "xsd")
# plt.plot(t, x(t,Iad,Qad,2.7e9), label = "xad")
# #plt.plot(t, x(t,Idelta,Qdelta,2.7e9), label = "xdelta")
# plt.legend()
# plt.xlabel('t')
# plt.ylabel('Données')
# plt.title('Tracé des signaux')
# plt.grid(True)
# plt.show()



### Transformées

# 1e étape : TF(x) et STFT (X)

t = np.linspace(0, len(sd)+1, 1000000)
# def STFT(x):
#     return stft(x,5e-9)
# fsd,Tsd,Zxxsd = STFT(x(t,Isd,Qsd,2.7e9))
# fad,Tad,Zxxad = STFT(x(t,Iad,Qad,2.7e9))
# plt.figure()
# plt.pcolormesh(Tsd, fsd, 10*np.log10(np.abs(Zxxsd)))
# plt.show()
# plt.figure()
# plt.pcolormesh(Tad, fad, 10*np.log10(np.abs(Zxxad)))
# plt.show()

a = x(t,Isd,Qsd,2.7e9)
Xsd = np.fft.fft(x(t,Isd,Qsd,2.7e9))
Xad = np.fft.fft(x(t,Iad,Qad,2.7e9))
# Xsd = np.fft.fftshift(Xsd)
# Xad = np.fft.fftshift(Xad)

fe = 1
plt.plot(np.linspace(-fe/2,fe/2,len(Xsd)), Xsd)
plt.plot(np.linspace(-fe/2,fe/2,len(Xsd)), Xad)
plt.show()