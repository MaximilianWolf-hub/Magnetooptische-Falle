import numpy as np
import scipy.optimize as opt
import tifffile as tiff


def gaussian_2D(XY, A, x0, y0, sigma_x, sigma_y):
    x, y = XY  # Entpacken der 2D-Koordinaten
    return A * np.exp(-((x - x0)**2 / (2 * sigma_x**2) + (y - y0)**2 / (2 * sigma_y**2)))

def fit_gaussian_2D(image):
    ny, nx = image.shape  # Bildgröße
    x = np.arange(nx)
    y = np.arange(ny)
    X, Y = np.meshgrid(x, y)  # 2D-Gitter für x- und y-Koordinaten

    # Bilddaten in 1D umwandeln
    xdata = X.ravel()
    ydata = Y.ravel()
    zdata = image.ravel()

    ### 3. Startwerte für den Fit ###
    p0 = [np.max(image), nx // 6, ny * 2 // 3, nx / 4, ny / 4]  # Schätzung für Parameter

    ### 4. Curve Fit ausführen ###
    params, cov = opt.curve_fit(gaussian_2D, (xdata, ydata), zdata, p0=p0)
    return params

def background_average(hintergrund):

    average = []
    ny, nx = 0, 0
    for datei in hintergrund:
        bild = tiff.imread(datei)
        average.append(np.mean(bild))
        ny, nx = bild.shape  # Bildgröße
    average = np.mean(average)
    return np.full((ny, nx), average)

