import numpy as np

# TODO: load constants from astropy
# Constants in SI units
h = 6.62607015e-34  # Planck constant, J·s
c = 299792458       # Speed of light, m/s
k = 1.380649e-23    # Boltzmann constant, J/K

def blackbody_radiation(wavelength, temp):
    """
    Calculates the spectral radiance of a black body at a given wavelength and temperature using Planck's law.
    
    Parameters:
    - wavelength: Wavelength of the radiation (in meters).
    - temp: Temperature of the black body (in Kelvin).
    
    Returns:
    - Spectral radiance (in W/m^2/sr/m) of the black body.
    """
    exponent_factor = np.exp(h * c / (wavelength * k * temp))
    spectral_radiance = (2 * h * c**2) / (wavelength**5 * (exponent_factor - 1))
    return spectral_radiance

def peak_wavelength(temp):
    """
    Calculates the peak wavelength of black body radiation for a given temperature using Wien's Law.
    
    Parameters:
    - temp: The absolute temperature of the black body (in Kelvin).
    
    Returns:
    - The peak wavelength (in meters).
    """
    b = 2.897e-3  # Wien's displacement constant in meter-Kelvin
    lambda_max = b / temp
    return lambda_max

def cobe_best_fit(frequencies, intensities, degree=3):
    """
    Calculates the best-fit polynomial coefficients for the COBE data.
    
    Parameters:
    - frequencies: Array of frequency data.
    - intensities: Array of intensity data.
    - degree: Degree of the polynomial to fit (default is 3 for a cubic polynomial).
    
    Returns:
    - Array of coefficients for the best-fit polynomial.
    """
    # Fit a polynomial of specified degree to the data
    coefficients = np.polyfit(frequencies, intensities, degree)
    return coefficients
