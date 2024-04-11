import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, Dropdown

from . import blackbody, const

PROVIDED_COLOR = 'C0'
STUDENT_COLOR = 'C1'
REFERENCE_COLOR = 'C2'

def blackbody_plot(wavelengths, ref_name, ref_temp, temp, bb_student_fn):
    ref_radiance = np.array([blackbody.radiation_law_wavelength(wavelength, ref_temp) for wavelength in wavelengths])
    # Calculate spectral radiance using the provided function
    provided_radiance = np.array([blackbody.radiation_law_wavelength(wavelength, temp) for wavelength in wavelengths])
    
    # Attempt to calculate spectral radiance using the student's function
    student_radiance = np.array([bb_student_fn(wavelength, temp) for wavelength in wavelengths])

    # Plot provided function results
    plt.plot(wavelengths * 1e9, provided_radiance, label='Provided Function', c=PROVIDED_COLOR)
    
    # Plot reference results
    plt.plot(wavelengths * 1e9, ref_radiance, label=f"{ref_name}'s Blackbody", linestyle='--', c=REFERENCE_COLOR)

    # Check if the student function returns valid results and plot if so
    if np.any(student_radiance != None):
        plt.plot(wavelengths * 1e9, student_radiance, label='Your Function', c=STUDENT_COLOR)

    plt.title('Blackbody Radiation Spectrum at {:.0f} K'.format(temp))
    plt.xlabel('Wavelength (nm)')
    plt.ylabel(r'Spectral Radiance ($W/m^2/sr/m$)')
    plt.legend(loc='upper right')
    plt.grid(True)

def blackbody_radiation(wavelengths, ref_name, ref_temp, temp, student_fn):
    """
    Plots the spectral radiance of a black body at given wavelengths and temperature,
    using both a provided reference function and the student's function.
    
    Parameters:
    - wavelengths: Array of wavelengths (in meters) to plot.
    - ref_name: Name of a reference object.
    - ref_temp: Temperature of a reference object (in Kelvin).
    - temp: Temperature of the black body (in Kelvin).
    - student_fn: Student's implementation of the black body radiation law.
    """

    blackbody_plot(wavelengths, ref_name, ref_temp, temp, student_fn)
    
    plt.show()

def interactive_blackbody_radiation(wavelengths, student_fn):
    """
    Creates an interactive plot for black body radiation with a slider to adjust the temperature.
    
    Parameters:
    - wavelengths: Array of wavelengths (in meters) to plot.
    - student_fn: Student's implementation of the black body radiation law.
    """
    
    # Create dropdown for reference temperature selection
    ref_dropdown = Dropdown(
        options=[(name, (name, temp)) for name, temp in const.reference_objects],
        value=("Sun", 5778),  # Default value
        description='Reference:'
    )

    def update_plot(temp=5778, ref=ref_dropdown.value):
        ref_name, ref_temp = ref
        blackbody_radiation(wavelengths, ref_name, ref_temp, temp, student_fn)
        
    temp_slider = FloatSlider(value=5778, min=1000, max=10000, step=100, description='Temp (K):', readout_format='.0f')
    
    interact(update_plot, temp=temp_slider, ref=ref_dropdown)

def peak_wavelength(wavelengths, ref_name, ref_temp, temp, bb_student_fn, wl_student_fn):
    """
    Plots the spectral radiance of a black body at given wavelengths and temperature,
    using both a provided reference function and the student's function, highlighting its peak.
    
    Parameters:
    - wavelengths: Array of wavelengths (in meters) to plot.
    - ref_name: Name of a reference object.
    - ref_temp: Temperature of a reference object (in Kelvin).
    - temp: Temperature of the black body (in Kelvin).
    - bb_student_fn: Student's implementation of the blackbody radiation.
    - wl_student_fn: Student's implementation of the wien's law.
    """
    
    blackbody_plot(wavelengths, ref_name, ref_temp, temp, bb_student_fn)

    # Calculate and plot the peak wavelength using blackbody.peak_wavelength
    peak_wavelength = blackbody.peak_wavelength(temp)
    peak_radiance = blackbody.radiation_law_wavelength(peak_wavelength, temp)
    plt.scatter(peak_wavelength * 1e9, peak_radiance, c=PROVIDED_COLOR, s=100, zorder=5, label='Provided Peak Wavelength')
    plt.annotate(f'Provided Peak at {peak_wavelength * 1e9:.2f} nm',
                 xy=(peak_wavelength * 1e9, peak_radiance),
                 xytext=(peak_wavelength * 1e9 * 1.5, peak_radiance * 0.7),
                 textcoords='data',
                 arrowprops=dict(arrowstyle='->', color=PROVIDED_COLOR))

    student_peak_wavelength = wl_student_fn(temp)
    student_peak_radiance = bb_student_fn(student_peak_wavelength, temp)
    if student_peak_wavelength is not None and student_peak_radiance is not None:
        plt.scatter(student_peak_wavelength * 1e9, student_peak_radiance, c=STUDENT_COLOR, s=100, marker='*', zorder=6, label='Your Peak Wavelength')
        plt.annotate(f'Your Peak at {student_peak_wavelength * 1e9:.2f} nm',
                    xy=(student_peak_wavelength * 1e9, peak_radiance),
                    xytext=(student_peak_wavelength * 1e9 * 1.3, student_peak_radiance * 0.9),
                    textcoords='data',
                    arrowprops=dict(arrowstyle='->', color=STUDENT_COLOR))

    # Define spectral regions with colors
    plt.axvspan(0, 400, color='violet', alpha=0.2, label='Ultraviolet')
    plt.axvspan(400, 700, color='yellow', alpha=0.2, label='Visible Light')
    plt.axvspan(700, 2000, color='red', alpha=0.2, label='Infrared')

    plt.legend(loc='upper right')
    plt.show()

def interactive_peak_wavelength(wavelengths, bb_student_fn, wl_student_fn):
    """
    Creates an interactive plot for black body radiation with a slider to adjust the temperature.
    
    Parameters:
    - wavelengths: Array of wavelengths (in meters) to plot.
    - bb_student_fn: Student's implementation of the blackbody radiation.
    - wl_student_fn: Student's implementation of the wien's law.
    """
    
    # Create dropdown for reference temperature selection
    ref_dropdown = Dropdown(
        options=[(name, (name, temp)) for name, temp in const.reference_objects],
        value=("Sun", 5778),  # Default value
        description='Reference:'
    )

    def update_plot(temp=5778, ref=ref_dropdown.value):
        ref_name, ref_temp = ref
        peak_wavelength(wavelengths, ref_name, ref_temp, temp, bb_student_fn, wl_student_fn)
        
    temp_slider = FloatSlider(value=5778, min=1000, max=10000, step=100, description='Temp (K):', readout_format='.0f')
    
    interact(update_plot, temp=temp_slider, ref=ref_dropdown)