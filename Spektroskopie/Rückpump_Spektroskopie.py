import numpy as np
import matplotlib.pyplot as plt

piezo = np.genfromtxt('Dispersionssignal_RL.csv', delimiter=',', skip_header=17, dtype=float)
rückp = np.genfromtxt('Spektroskopie_Rückpump.csv', delimiter=',', skip_header=17, dtype=float)




piezo = piezo[~np.isnan(piezo)]
piezo = piezo.reshape(-1, 4)

rückp = rückp[~np.isnan(rückp)]
rückp = rückp.reshape(-1, 4)

plt.plot(rückp[330:-70, 0], rückp[330:-70, 3])
plt.xlabel('Zeit in s')
plt.ylabel('Spannung in V')
#plt.plot(piezo[:, 0], piezo[:, 1])
plt.show()
