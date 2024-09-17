import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft # short time fourier transform to have time and frequency

#Parametres
fe=1000 #freq echantillonage
T=7 #duree
t=np.linspace(0,T,fe*T)

#parametres du drone
c_son = 3*10**8
f_radar= 15*10**9
lam=c_son/f_radar
v_ensemble = 0.5
lbda=0.02 # c/f avec f frequece de radar 15GHz
doppler_ensemble = v_ensemble *2 /0.02 #approximation de l'effet doppler d'un mouvement lineaire fd=2v/lambda

f_rotor =5
amp_rotor=1
doppler_rotor=amp_rotor*np.sin(2*np.pi*f_rotor*t)
doppler = doppler_rotor + doppler_ensemble

signal = np.cos(doppler*t)


f,t_spec, Zxx = stft(signal,fe,nperseg=256) #nperseg = longueur de la fenetre

plt.pcolormesh(t_spec,f, np.abs(Zxx),shading='gouraud',cmap='inferno')
plt.title('simulation1 de la signature micro-doppler du drone')
plt.ylabel('Freq (Hz)')
plt.xlabel('temps(s)')
plt.show()

###WSHHHH CA TOURNE PASS!!!!

plt.pcolormesh(t_spec,f, np.abs(Zxx),shading='gouraud',cmap='inferno')
plt.title('zoom simulation de la signature micro-doppler du drone')
plt.ylabel('Freq (Hz)')
plt.xlabel('temps(s)')
plt.ylim([0,50])
plt.show()

plt.plot(t_spec,f)
plt.title('simulation2 de la signature micro-doppler du drone')
plt.ylabel('Freq (Hz)')
plt.xlabel('temps(s)')
plt.show()