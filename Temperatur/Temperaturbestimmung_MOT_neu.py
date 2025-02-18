import numpy as np
from uncertainties import ufloat
import matplotlib.pyplot as plt
import tifffile as tiff
import glob
from Temperatur.Funktionen import background_average, fit_gaussian_2D
import re
from scipy.optimize import curve_fit



messung_1 = glob.glob(r"C:\Users\Maximilian Wolf\Desktop\Uni\FP\Magnetooptische Falle\Wolf_Hesse\Ersatzdaten\240601\Temperaturbestimmung Melasse\images_0003\Images\*.tiff")
messung_1.sort(key=lambda f: float(re.search(r"tof_(\d+\.\d+)ms", f).group(1)))






hintergrund_1 = glob.glob(r"C:\Users\Maximilian Wolf\Desktop\Uni\FP\Magnetooptische Falle\Wolf_Hesse\Ersatzdaten\240601\Temperaturbestimmung Melasse\images_0003\Background\*.tiff")

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

Verlauf_sigma_x_square = Verlauf_sigma_x**2
Verlauf_sigma_y_square = Verlauf_sigma_y**2

#Festlegenn der Zeitskala (0 - 5ms)
time = np.arange(0, 5.1, 0.25)
time_square = time ** 2

#Latex für Graphenbeschriftung
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

#definition des linearen Fit Modells
def linear_fit(x, m, b):
    return m * x + b

#Startwerte für den linearen Fit an \sigma^2 und T^2
p0_x = [max(Verlauf_sigma_x_square) - min(Verlauf_sigma_x_square) / max(time_square), min(Verlauf_sigma_x_square)]
p0_y = [max(Verlauf_sigma_y_square) - min(Verlauf_sigma_y_square) / max(time_square), min(Verlauf_sigma_y_square)]

params_x, cov_x = curve_fit(linear_fit, (time_square), Verlauf_sigma_x_square, p0_x)
params_y, cov_y = curve_fit(linear_fit, (time_square), Verlauf_sigma_y_square, p0_y)

#Unsicherheiten aus der Kovarianzmatrix berechnen
perr_x = np.sqrt(np.diag(cov_x))
perr_y = np.sqrt(np.diag(cov_y))

Steigung_x = ufloat(params_x[0], perr_x[0])
Steigung_y = ufloat(params_y[0], perr_y[0])

lin_fit_x = linear_fit(time_square, params_x[0], params_x[1])
lin_fit_y = linear_fit(time_square, params_y[0], params_y[1])

print('Steigung sigma_x: ', Steigung_x, 'Steigung sigma_y: ', Steigung_y)

Temperatur_x = 1e6 * Steigung_x * 84.912 * 1.66e-27 / 1.38e-23
Temperatur_y = 1e6 * Steigung_y * 84.912 * 1.66e-27 / 1.38e-23

print('Temperatur_x: ', Temperatur_x, 'Temperatur_y: ', Temperatur_y)

#Plotten der Daten
plt.plot(time_square, Verlauf_sigma_x_square)
plt.plot(time_square, Verlauf_sigma_y_square)
plt.plot(time_square, lin_fit_x)
plt.plot(time_square, lin_fit_y)
plt.xlabel('$\mathrm{T}^2$ in $\mathrm{ms}^2$')
plt.ylabel(r"$\sigma_x^2$ und $\sigma_y^2$ in $\mathrm{m}^2$")
plt.savefig('Messung_1_Temperatur_MOT.png')
plt.show()


