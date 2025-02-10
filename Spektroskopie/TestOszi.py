import numpy as np
import matplotlib.pyplot as plt


datei = np.genfromtxt('nur_Rb85_Dip.csv', delimiter=',', skip_header=17, dtype=float)




datei = datei[~np.isnan(datei)]
datei = datei.reshape(-1, 4)

#plt.plot(datei[:, 0], datei[:, 3])
plt.plot(datei[:, 0], datei[:, 1])
plt.show()
print(datei)

print(1e6 * 8.23e-9 * 84.912 * 1.66e-27 / 1.38e-23)

