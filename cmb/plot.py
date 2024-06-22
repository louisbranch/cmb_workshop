import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, Dropdown, FloatSlider, Label, VBox, HBox, Output
from IPython.display import display, Math

from . import functions, const, cmb_utils

PROVIDED_COLOR = 'C0'
STUDENT_COLOR = 'C1'
REFERENCE_COLOR = 'C2'

def blackbody_plot(wavelengths, ref_name, ref_temp, temp, bb_student_fn):
    ref_radiance = np.array([functions.blackbody_radiation(wavelength, ref_temp) for wavelength in wavelengths])
    # Calculate spectral radiance using the provided function
    provided_radiance = np.array([functions.blackbody_radiation(wavelength, temp) for wavelength in wavelengths])
    
    # Attempt to calculate spectral radiance using the student's function
    student_radiance = np.array([bb_student_fn(wavelength, temp) for wavelength in wavelengths])

    # Plot provided function results
    plt.plot(wavelengths * 1e9, provided_radiance, label='Provided Blackbody Function', c=PROVIDED_COLOR)
    
    # Plot reference results
    plt.plot(wavelengths * 1e9, ref_radiance, label=f"{ref_name}'s Blackbody", linestyle='--', c=REFERENCE_COLOR)

    # Check if the student function returns valid results and plot if so
    if np.any(student_radiance != None):
        plt.plot(wavelengths * 1e9, student_radiance, label='Your Blackbody Function', c=STUDENT_COLOR)

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
    peak_radiance = functions.blackbody_radiation(peak_wavelength, temp)
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
                    xy=(student_peak_wavelength * 1e9, student_peak_radiance),
                    xytext=(student_peak_wavelength * 1e9 * 1.3, student_peak_radiance * 0.9),
                    textcoords='data',
                    arrowprops=dict(arrowstyle='->', color=STUDENT_COLOR))

    # Define spectral regions with colors
    plt.axvspan(0, 400, color='violet', alpha=0.2, label='Ultraviolet')
    plt.axvspan(400, 700, color='yellow', alpha=0.2, label='Visible Light')
    plt.axvspan(700, 2000, color='red', alpha=0.2, label='Infrared')

    plt.legend(loc='upper right')
    plt.show()

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

def cobe_curve_fit(temp, bb_student_fn, output):

    with output:
        output.clear_output(wait=True)

        data = const.cmb_cobes
        frequencies = data[:, 0]
        intensities = data[:, 1]
        wavelengths = np.array([functions.convert_to_freq_cm(freq) for freq in frequencies])
        wavelengths = np.array([functions.convert_to_freq_cm(freq) for freq in frequencies])

        plt.scatter(frequencies, intensities, color=PROVIDED_COLOR, label='COBE Data')

        provided_radiance = np.array([functions.blackbody_radiation(wavelength, temp) for wavelength in wavelengths])
        student_radiance = np.array([bb_student_fn(wavelength, temp) for wavelength in wavelengths])
        
        if np.any(student_radiance != None):
            intensity_mjy_sr = np.array([functions.convert_to_mjy_sr(sr, wl) for sr, wl in zip(student_radiance, wavelengths)])
            plt.plot(frequencies, intensity_mjy_sr, label='Your Blackbody Function', c=STUDENT_COLOR)
        else:
            intensity_mjy_sr = np.array([functions.convert_to_mjy_sr(sr, wl) for sr, wl in zip(provided_radiance, wavelengths)])
            plt.plot(frequencies, intensity_mjy_sr, label='Provided Blackbody Function', c=PROVIDED_COLOR)

        plt.title(f'Cosmic microwave background spectrum (from COBE)')
        plt.xlabel(r'Frequency ($cm^{-1}$)')
        plt.ylabel('Intensity (MJy/sr)')
        plt.legend()
        plt.grid(True)
        plt.show()

def redshift_visualization(velocity, output):
    with output:
        output.clear_output(wait=True)

        # Constants
        c = 3e8  # Speed of light in m/s
        initial_wavelength = 500  # Initial wavelength in nm (green light)
        
        # Calculate the shifted wavelength
        shifted_wavelength = initial_wavelength * np.sqrt((1 + velocity/c) / (1 - velocity/c))
        
        # Plotting the initial and shifted spectrum
        fig, ax = plt.subplots()
        
        # Initial spectrum
        x_initial = np.linspace(400, 700, 1000)
        y_initial = np.exp(-0.5 * ((x_initial - initial_wavelength) / 10)**2)
        ax.plot(x_initial, y_initial, label='Initial Spectrum', color='green')
        
        # Shifted spectrum
        y_shifted = np.exp(-0.5 * ((x_initial - shifted_wavelength) / 10)**2)
        ax.plot(x_initial, y_shifted, label='Shifted Spectrum', color='red' if velocity > 0 else 'blue')
        
        # Adding labels and legend
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Intensity')
        ax.legend()

        # Format the velocity as powers of ten
        if velocity == 0:
            velocity_power_ten = "0"
        else:
            exponent = int(np.log10(abs(velocity)))
            base = velocity / 10**exponent
            velocity_power_ten = "{:.2f} x $10^{}$".format(base, exponent)
        ax.set_title(fr'Galaxy Moving {"Away" if velocity > 0 else "Towards"} (Velocity = {velocity_power_ten} m/s)')

        plt.show()

def planck_map(fits='COM_CMB_IQU-commander_1024_R2.02_dg16_car.fits'):
    map = cmb_utils.load_cmb_map(f'data/{fits}')
    cmb_utils.view_map(map)

    return map

def cmb_std_dev(data, show_guidelines=False):
    
    mean = np.mean(data)
    std = np.std(data)
    
    flattened_data = data.flatten()
    
    plt.hist(flattened_data, bins=100, alpha=0.7)
    
    plt.axvline(mean, color='blue', linestyle='--', label=f'Mean')
    
    if show_guidelines:
        plt.axvline(mean + std, color='green', linestyle=':', label='1σ')
        plt.axvline(mean - std, color='green', linestyle=':')
        plt.axvline(mean + 2 * std, color='orange', linestyle=':', label='2σ')
        plt.axvline(mean - 2 * std, color='orange', linestyle=':')
        plt.axvline(mean + 3 * std, color='purple', linestyle=':', label='3σ')
        plt.axvline(mean - 3 * std, color='purple', linestyle=':')

    plt.xlabel('Temperature Fluctuations (K)')
    plt.ylabel('Count')
    plt.title('Temperature Fluctuations in CMB Data')
    plt.legend()
    plt.grid(False)

    # Set the x-ticks with the central tick at 0 and others around it
    max_tick = max(abs(data.min()), data.max())
    ticks = np.arange(-max_tick, max_tick, std)
    plt.xticks(ticks)
    plt.gca().set_xticklabels([f'{x:.5f}' for x in plt.gca().get_xticks()], rotation=45)

    plt.show()