from pixell import colorize
from pixell import enmap
from scipy import ndimage
from pixell import enmap
import matplotlib.pyplot as plt
import numpy as np

from pixell import reproject, colorize

from .i18n import I18N
i18n = I18N()

# try registering a new colormap, pass if it exists
try:
    colorize.mpl_register("planck")
except:
    pass

def load_cmb_map(filename):
    imap = enmap.read_map(filename)
    return imap[0]

def view_map(imap, size=(40, 10)):
    fig = plt.figure(figsize=size)
    ax = fig.add_subplot(111, projection=imap.wcs)
    ax.imshow(imap, origin="lower", cmap="planck")
    ax.axis("off")
    plt.show()

def find_maxima(imap, neighborhood_size=100, n_threshold=2):
    # defines the radius in which we search for a local maximum
    rms = np.std(imap)
    threshold = 2 * n_threshold
    imap_max = ndimage.maximum_filter(imap, neighborhood_size)
    maxima = (imap == imap_max)
    maxima[maxima < threshold] = 0
    # data_min = filters.minimum_filter(data, neighborhood_size)
    # diff = ((data_max - data_min) > threshold)
    # maxima[diff == 0] = 0
    labeled, num_objects = ndimage.label(maxima)
    xy = np.array(ndimage.center_of_mass(imap, labeled, range(1, num_objects+1)))
    coords = imap.pix2sky(xy.T).T
    return coords

def extract_thumbnails(imap, coords):
    # assume coords are in degs
    x, y = np.deg2rad(coords).T
    # assume coords are in x, y format, but our subsequent 
    # code assumes y, x, so we need to swap the order now
    coords = np.array([y, x]).T
    # now extract the thumbnails
    thumbnails = reproject.thumbnails(imap, coords, r=np.deg2rad(1), apod=0)
    return thumbnails

def plot_thumbnails(thumbnails, ncol=5, figsize=(10,10)):
    fig = plt.figure(figsize=figsize)
    nrow = int(np.ceil(len(thumbnails) / ncol))
    for i, thumb in enumerate(thumbnails):
        ax = fig.add_subplot(nrow, ncol, i + 1, projection=thumb.wcs)
        ax.imshow(thumb, cmap="planck")
        ax.axis('off')
        ax.set_title(i18n.gettext("thumbnail_title").format(i + 1), fontsize=10)
    plt.tight_layout()
    plt.show()

def extract_profile(mean_img):
    r = np.rad2deg(mean_img.modrmap())
    bins = np.linspace(0, 1, 20)
    idx = np.digitize(r, bins)
    mean_profile = np.array([np.mean(mean_img[idx == k]) for k in range(1, len(bins))])
    bin_centers = (bins[1:] + bins[:-1])/2
    return bin_centers, mean_profile * 1e6  # uK

def measure_profile(x, profile):
    from ipywidgets import interact

    @interact(v=100.0)
    def fun(v=100):
        plt.plot(x, profile)
        plt.axhline(v)
        plt.ylabel(i18n.gettext("ylabel_temperature"))
        plt.xlabel(i18n.gettext("xlabel_degrees"))
    return fun

def H_a(a, H_0, Omega_m, Omega_lambda, Omega_r):
    return H_0 * (Omega_m * a**-3 + Omega_lambda + Omega_r * a**-4)**0.5

def measure_distance(h_0=70):
    from scipy import integrate
    from ipywidgets import interact 
    from astropy.cosmology import Planck18 as cosmo

    @interact(H_0=h_0)
    def fun(H_0):
        a_recomb = 1 / (1 + 1100)

        integrand = lambda a: 1 / (a**2 * H_a(a, H_0, cosmo.Om0, cosmo.Ode0, cosmo.Ogamma0) / 3e5)
        comoving_dist = integrate.quad(integrand, a_recomb, 1)[0]
        print(i18n.gettext("distance_to_recombination").format(comoving_dist))

        integrand = lambda a: 1 / (a * H_a(a, H_0, cosmo.Om0, cosmo.Ode0, cosmo.Ogamma0) / 3e5)
        physical_dist = integrate.quad(integrand, a_recomb, 1)[0]
        c = 3.06e-7  # Mpc/yr
        print(i18n.gettext("travel_time_to_recombination").format(physical_dist / c / 1e9))

    return fun
