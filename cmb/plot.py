import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed, Dropdown, FloatSlider, IntSlider

from . import functions, const

PROVIDED_COLOR = 'C0'
STUDENT_COLOR = 'C1'
REFERENCE_COLOR = 'C2'

def blackbody_plot(wavelengths, ref_name, ref_temp, temp, bb_student_fn):
    ref_radiance = np.array([functions.radiation_law_wavelength(wavelength, ref_temp) for wavelength in wavelengths])
    # Calculate spectral radiance using the provided function
    provided_radiance = np.array([functions.radiation_law_wavelength(wavelength, temp) for wavelength in wavelengths])
    
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

def interactive_blackbody_radiation(student_fn, wavelengths=const.wavelengths):
    """
    Creates an interactive plot for black body radiation with a slider to adjust the temperature.
    
    Parameters:
    - student_fn: Student's implementation of the black body radiation law.
    - wavelengths: Array of wavelengths (in meters) to plot.
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
    peak_wavelength = functions.peak_wavelength(temp)
    peak_radiance = functions.radiation_law_wavelength(peak_wavelength, temp)
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

def interactive_peak_wavelength(bb_student_fn, wl_student_fn, wavelengths=const.wavelengths):
    """
    Creates an interactive plot for black body radiation with a slider to adjust the temperature.
    
    Parameters:
    - bb_student_fn: Student's implementation of the blackbody radiation.
    - wl_student_fn: Student's implementation of the wien's law.
    - wavelengths: Array of wavelengths (in meters) to plot.
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

def visibile_wavelengths():
    # Defining the visible light spectrum in nm and their corresponding colors
    wavelengths = [400, 450, 495, 570, 590, 620, 700]
    colors = ['#8B00FF', '#4B0082', '#00FF00', '#FFFF00', '#FF7F00', '#FF0000']
    labels = ['Violet', 'Blue', 'Green', 'Yellow', 'Orange', 'Red']

    # Create a figure and a single subplot
    fig, ax = plt.subplots(figsize=(20, 2))

    # Plot each segment in its respective color
    for i in range(len(wavelengths) - 1):
        ax.axvspan(wavelengths[i], wavelengths[i + 1], color=colors[i], alpha=0.5)
        # Adding annotations approximately in the middle of each color band
        ax.text((wavelengths[i] + wavelengths[i + 1]) / 2, 1, labels[i], 
                color='black', horizontalalignment='center', verticalalignment='center')

    # Setting labels and title
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Intensity (arbitrary units)')
    ax.set_xticks(wavelengths)
    ax.set_title('Visible Light Spectrum')

    # Limiting the x-axis to the visible spectrum range
    ax.set_xlim(400, 700)
    ax.set_ylim(0, 2)

    # Remove y-axis for cleaner visualization
    ax.yaxis.set_visible(False)

    plt.show()

def cobe_coefficients_fit(coeffs=None, show_best_fit=False):
    """
    Plots COBE data points and a forth-degree polynomial fit based on provided coefficients.
    
    Parameters:
    - coeffs: coefficients of the polynomial
    """

    data = const.cmb_cobes
    frequencies = data[:, 0]
    intensities = data[:, 1]

    plt.scatter(frequencies, intensities, color=PROVIDED_COLOR, label='COBE Data')
    
    # Generate a range of frequency values for plotting the fit curve
    freq_range = np.linspace(frequencies.min(), frequencies.max(), 400)
    
    # Calculate the values of the polynomial at each point in freq_range
    if coeffs is not None:
        a, b, c, d, e = coeffs
        fit_curve = a*freq_range**4 + b*freq_range**3 + c*freq_range**2 + d*freq_range + e
    
        # Plot the polynomial fit curve
        plt.plot(freq_range, fit_curve, color=STUDENT_COLOR, label='Fit Curve')

    # Optionally plot the best fit curve
    if show_best_fit:
        best_fit_coeffs = functions.cobe_best_fit(frequencies, intensities, 5)
        best_fit_curve = np.polyval(best_fit_coeffs, freq_range)
        plt.plot(freq_range, best_fit_curve, label='Best Fit', color=REFERENCE_COLOR, linestyle='--')

    plt.title('Cosmic microwave background spectrum (from COBE)')
    plt.xlabel('Frequency (cm^-1)')
    plt.ylabel('Intensity (MJy/sr)')
    plt.legend()
    plt.grid(True)
    plt.show()

def interactive_cobe_polynomial_fit():
    """
    Creates interactive controls for fitting polynomial and showing best fit.
    """

    a = FloatSlider(min=-0.05, max=0, step=0.01, value=-0.05, description='a: x^4')
    b = FloatSlider(min=2.2, max=2.3, step=0.01, value=2.2, description='b: x^3')
    c = FloatSlider(min=-43, max=-42, step=0.1, value=-43, description='c: x^2')
    d = FloatSlider(min=280, max=285, step=0.5, value=280, description='d: x')
    e = FloatSlider(min=-250, max=-240, step=1, value=-250, description='e')
    
    def update_plot(a, b, c, d, e, show_best_fit):
        cobe_coefficients_fit((a, b, c, d, e), show_best_fit)
    
    interact(update_plot, a=a, b=b, c=c, d=d, e=e, show_best_fit=fixed(False))


def cobe_degree_fit(degree):
    """Fit a polynomial of specified degree to the data and plot the results."""

    data = const.cmb_cobes
    frequencies = data[:, 0]
    intensities = data[:, 1]

    # Fit polynomial
    coeffs = np.polyfit(frequencies, intensities, degree)
    
    # Generate polynomial curve
    freq_range = np.linspace(min(frequencies), max(frequencies), 400)
    fit_curve = np.polyval(coeffs, freq_range)
    
    # Plot data
    plt.scatter(frequencies, intensities, color=PROVIDED_COLOR, label='COBE Data')
    plt.plot(freq_range, fit_curve, color=STUDENT_COLOR, label=f'{degree}-degree Fit')
    plt.title(f'Cosmic microwave background spectrum (from COBE)\n{degree}-degree Polynomial Fit')
    plt.xlabel('Frequency')
    plt.ylabel('Intensity')
    plt.legend()
    plt.grid(True)
    plt.show()

def interactive_polynomial_degree_selector():
    """Interactive selector for polynomial degree."""
    slider = IntSlider(min=1, max=5, step=1, value=1, description='Polynomial Degree', 
                       style={'description_width': '150px'})
    interact(cobe_degree_fit, degree=slider)