import numpy as np
import matplotlib.pyplot as plt


def read_iq_file(file_path, data_type=np.float32):
    # Lire le fichier binaire
    iq_data = np.fromfile(file_path, dtype=data_type)

    # Séparer les échantillons I et Q
    I = iq_data[0::2]
    Q = iq_data[1::2]

    return I, Q


# Spécifiez le chemin du fichier IQ
file_path = "C:\Applis\PyCharm\Projects\MDCP\Data\exp1_22.10.24SansDronecentre2.7GHz.iq"

# Lire les échantillons I et Q
I_samples, Q_samples = read_iq_file(file_path)

# Tracer Q en fonction de I
plt.figure(figsize=(10, 6))
plt.plot(I_samples, Q_samples, 'o', markersize=1)
plt.title('Tracé de Q en fonction de I')
plt.xlabel('I')
plt.ylabel('Q')
plt.grid(True)
plt.show()