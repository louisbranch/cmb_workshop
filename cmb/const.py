import numpy as np

from .i18n import I18N
i18n = I18N()

# Constants in SI units
h = 6.62607015e-34  # Planck constant, J·s
c = 299792458       # Speed of light, m/s
k = 1.380649e-23    # Boltzmann constant, J/K
moon_r = 1737.1e3   # Radius of the Moon, m
moon_angular_size = 0.00908 # Angular size of the Moon, rad

wavelengths = np.linspace(100e-9, 2000e-9, 100) # 100 points from 100 nm to 2000 nm

reference_objects = [
    (i18n.gettext("object_sun"), 5778),
    (i18n.gettext("object_sirius_a"), 9940),
    (i18n.gettext("object_red_dwarf"), 3200)
]

# COBE/FIRAS CMB monopole spectrum
# frequency[cm^-1] by intensity [MJy/sr]
# source: https://lambda.gsfc.nasa.gov/data/cobe/firas/monopole_spec/firas_monopole_spec_v1.txt
cmb_cobes = np.array([
    (2.27, 200.723),
    (2.72, 249.508),
    (3.18, 293.024),
    (3.63, 327.770),
    (4.08, 354.081),
    (4.54, 372.079),
    (4.99, 381.493),
    (5.45, 383.478),
    (5.90, 378.901),
    (6.35, 368.833),
    (6.81, 354.063),
    (7.26, 336.278),
    (7.71, 316.076),
    (8.17, 293.924),
    (8.62, 271.432),
    (9.08, 248.239),
    (9.53, 225.940),
    (9.98, 204.327),
    (10.44, 183.262),
    (10.89, 163.830),
    (11.34, 145.750),
    (11.80, 128.835),
    (12.25, 113.568),
    (12.71, 99.451),
    (13.16, 87.036),
    (13.61, 75.876),
    (14.07, 65.766),
    (14.52, 57.008),
    (14.97, 49.223),
    (15.43, 42.267),
    (15.88, 36.352),
    (16.34, 31.062),
    (16.79, 26.580),
    (17.24, 22.644),
    (17.70, 19.255),
    (18.15, 16.391),
    (18.61, 13.811),
    (19.06, 11.716),
    (19.51, 9.921),
    (19.97, 8.364),
    (20.42, 7.087),
    (20.87, 5.801),
    (21.33, 4.523)
])

cmb_map_url = 'https://phy-act1.princeton.edu/public/snaess/actpol/dr5/atlas/'

cmb_thumbnails_coords = np.array([
    [-46.266, -25.65],
    [-40.525, -21.99],
])

cmb_thumbnails_coords_extra = np.array([
    [-46.266, -25.65],
    [-40.525, -21.99],
    [-41.237, -20.341],
    [-37.013, -27.877],
    [-34.281, -30.20],
    [-38.623, -32.821],
    [-41.769, -33.936],
    [-42.954, -34.283],
    [-49.058, -34.883],
    [-49.985, -36.242],
    [-49.996, -38.113],
    [-49.258, -41.430],
    [-3.188, -42.858],
    [-6.204, -42.142],
    [16.714, -57.000],
])