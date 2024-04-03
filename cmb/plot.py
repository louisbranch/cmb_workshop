import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider
import ipywidgets as widgets

from . import blackbody

def blackbody_radiation(wavelengths, temp, student_fn):
    """
    Plots the spectral radiance of a black body at given wavelengths and temperature,
    using both a provided reference function and the student's function.
    
    Parameters:
    - wavelengths: Array of wavelengths (in meters) to plot.
    - temp: Temperature of the black body (in Kelvin).
    - student_fn: Student's implementation of the black body radiation law.
    """
    # Calculate spectral radiance of the Sun using the provided function
    sun_temp = 5772
    sun_radiance = np.array([blackbody.radiation_law_wavelength(wavelength, sun_temp) for wavelength in wavelengths])

    # Calculate spectral radiance using the provided function
    provided_radiance = np.array([blackbody.radiation_law_wavelength(wavelength, temp) for wavelength in wavelengths])
    
    # Attempt to calculate spectral radiance using the student's function
    student_radiance = np.array([student_fn(wavelength, temp) for wavelength in wavelengths])
    
    # Plot provided function results
    plt.plot(wavelengths * 1e9, provided_radiance, label='Provided Function')
    
    # Check if the student function returns valid results and plot if so
    if np.any(student_radiance != None):
        plt.plot(wavelengths * 1e9, student_radiance, label='Your Function')

    # Plot reference results
    plt.plot(wavelengths * 1e9, sun_radiance, label="Sun's Blackbody", linestyle='--')
    
    plt.title('Blackbody Radiation Spectrum at {:.0f} K'.format(temp))
    plt.xlabel('Wavelength (nm)')
    plt.ylabel(r'Spectral Radiance ($W/m^2/sr/m$)')
    plt.legend()
    plt.grid(True)
    plt.show()

def interactive_blackbody_radiation(wavelengths, student_fn):
    """
    Creates an interactive plot for black body radiation with a slider to adjust the temperature.
    
    Parameters:
    - wavelengths: Array of wavelengths (in meters) to plot.
    - student_fn: Student's implementation of the black body radiation law.
    """
    def update_plot(temp=5778):
        blackbody_radiation(wavelengths, temp, student_fn)
        
    temp_slider = FloatSlider(value=5778, min=1000, max=10000, step=100, description='Temp (K):', readout_format='.0f')
    
    interact(update_plot, temp=temp_slider)