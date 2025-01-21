import numpy as np
from scipy.signal import stft
import matplotlib.pyplot as plt

fs = 1024
t = np.arange(0, 1.0, 1.0 / fs)
x = np.sin(2 * np.pi * 100 * t) + np.sin(2 * np.pi * 200 * t)

f, t, Zxx = stft(x, fs=fs, nperseg=256)

plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
plt.ylabel('Hz')
plt.xlabel('Sec')
plt.show()
