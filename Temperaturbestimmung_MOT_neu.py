import numpy as np
import os
import matplotlib.pyplot as plt
import tifffile as tiff
import glob
from Funktionen import background_average, fit_gaussian_2D
import re

messung_1 = glob.glob(r"C:\Users\Maximilian Wolf\Desktop\Uni\FP\Magnetooptische Falle\Wolf_Hesse\Ersatzdaten\240601\Temperaturbestimmung MOT\images_0000\Images\*.tiff")
messung_1.sort(key=lambda f: float(re.search(r"tof_(\d+\.\d+)ms", f).group(1)))

hintergrund_1 = glob.glob(r"C:\Users\Maximilian Wolf\Desktop\Uni\FP\Magnetooptische Falle\Wolf_Hesse\Ersatzdaten\240601\Temperaturbestimmung MOT\images_0000\Background\*.tiff")

average_hint = background_average(hintergrund_1)


Verlauf_sigma_x = []
Verlauf_sigma_y = []


for mess in messung_1:
    img = tiff.imread(mess)
    img = img - average_hint
    data = fit_gaussian_2D(img)
    Verlauf_sigma_x.append(abs(data[3]))
    Verlauf_sigma_y.append(abs(data[4]))


#Anpassen, dass ein Pixel 6,7 Mikrometern entspricht
Verlauf_sigma_y = np.array(Verlauf_sigma_y) * 6.7e-6
Verlauf_sigma_x = np.array(Verlauf_sigma_x) * 6.7e-6

Verlauf_sigma_x = Verlauf_sigma_x**2
Verlauf_sigma_y = Verlauf_sigma_y**2

#Plotten der Daten
time = np.arange(0, 5.1, 0.25)
time = time ** 2
plt.plot(time, Verlauf_sigma_x)
plt.plot(time, Verlauf_sigma_y)
plt.show()
