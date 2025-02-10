import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import tifffile as tiff
import glob
import os
from PIL import Image

### 1. TIFF-Datei laden ###
image = tiff.imread("../tof_1.25ms_rep_0.tiff")  # Bild laden
ny, nx = image.shape  # Bildgröße
x = np.arange(nx)
y = np.arange(ny)
X, Y = np.meshgrid(x, y)  # 2D-Gitter für x- und y-Koordinaten

#Hintergrund
hintergrund = glob.glob(r"C:\Users\Maximilian Wolf\Desktop\Uni\FP\Magnetooptische Falle\Wolf_Hesse\Ersatzdaten\240601\Temperaturbestimmung MOT\images_0000\Background\*.tiff")

if hintergrund:
    average = []
    for datei in hintergrund:
        bild = tiff.imread(datei)
        average.append(np.mean(bild))
    print('Average: ', np.mean(average))
else:
    print("Keine Dateien gefunden.")


# Bilddaten in 1D umwandeln
xdata = X.ravel()
ydata = Y.ravel()
zdata = image.ravel()

### 2. 2D-Gauss-Funktion definieren ###
def gaussian_2D(XY, A, x0, y0, sigma_x, sigma_y):
    x, y = XY  # Entpacken der 2D-Koordinaten
    return A * np.exp(-((x - x0) ** 2 / (2 * sigma_x ** 2) + (y - y0) ** 2 / (2 * sigma_y ** 2)))

### 3. Startwerte für den Fit ###
p0 = [np.max(image), nx//6, ny//2, nx/4, ny/4]  # Schätzung für Parameter

### 4. Curve Fit ausführen ###
params, cov = opt.curve_fit(gaussian_2D, (xdata, ydata), zdata, p0=p0)

# Gefittete Parameter extrahieren
A_fit, x0_fit, y0_fit, sigma_x_fit, sigma_y_fit = params
print(f"Gefittete Parameter:\n A={A_fit}, x0={x0_fit}, y0={y0_fit}, sigma_x={sigma_x_fit}, sigma_y={sigma_y_fit}")

### 5. Gefittetes Modell berechnen ###
Z_fit = gaussian_2D((X, Y), *params).reshape(ny, nx)

### 6. Originalbild und Fit plotten ###
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ax[0].imshow(image, cmap="gray", origin="upper")
ax[0].set_title("Originalbild")

ax[1].imshow(Z_fit, cmap="gray", origin="upper")
ax[1].set_title("Gefittete 2D-Gauss-Funktion")

plt.show()
