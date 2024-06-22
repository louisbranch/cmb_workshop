import numpy as np
from ipywidgets import Dropdown, FloatSlider, interact, Output, Label, VBox, HBox
from IPython.display import display

from . import plot, const

def peak_wavelength(bb_student_fn, wl_student_fn, wavelengths=const.wavelengths):
    """
    Creates an interactive plot for black body radiation with a slider to adjust the temperature.
    
    Parameters:
    - bb_student_fn: Student's implementation of the blackbody radiation.
    - wl_student_fn: Student's implementation of the wien's law.
    - wavelengths: Array of wavelengths (in meters) to plot.
    """
    
    ref_dropdown = Dropdown(
        options=[(name, (name, temp)) for name, temp in const.reference_objects],
        value=("Sun", 5778),  # Default value
        description='Reference:',
        tooltip='Reference object to compare with.'
    )

    def update_plot(temp=5778, ref=ref_dropdown.value):
        ref_name, ref_temp = ref
        plot.peak_wavelength(wavelengths, ref_name, ref_temp, temp, bb_student_fn, wl_student_fn)
        
    temp_slider = FloatSlider(
        value=5778,
        min=1000,
        max=10000,
        step=100,
        description='Temp (K):',
        readout_format='.0f',
        tooltip='Temperature of the black body.'
    )
    
    interact(update_plot, temp=temp_slider, ref=ref_dropdown)

def blackbody_radiation(student_fn, wavelengths=const.wavelengths):
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
        description='Reference:',
        tooltip='Reference object to compare with.'
    )

    temp_slider = FloatSlider(
        value=5778,
        min=1000,
        max=10000,
        step=100,
        description='Temp (K):',
        readout_format='.0f',
        tooltip='Temperature of the black body.'
    )

    def update_plot(temp=5778, ref=ref_dropdown.value):
        ref_name, ref_temp = ref
        plot.blackbody_radiation(wavelengths, ref_name, ref_temp, temp, student_fn)
        
    interact(update_plot, temp=temp_slider, ref=ref_dropdown)

def redshift():
    output = Output()

    slider = FloatSlider(
        value=0,
        min=-8e7,
        max=1e8,
        step=1e6,
        description='Velocity (m/s)',
        readout=False,
        tootltip='Velocity of the galaxy'
    )

    velocity_label = Label()

    def update_label(change):
        velocity = change['new']
        if velocity == 0:
            velocity_power_ten = "0"
        else:
            exponent = int(np.log10(abs(velocity)))
            base = velocity / 10**exponent
            velocity_power_ten = "{:.2f} x 10^{}".format(base, exponent)
        velocity_label.value = f"{velocity_power_ten} m/s"

    def update_plot(change):
        plot.redshift_visualization(change['new'], output)

    slider.observe(update_label, names='value')

    update_label({'new': slider.value})

    output = Output()

    ui = VBox([HBox([slider, velocity_label]), output])

    slider.observe(update_plot, names='value')

    display(ui)

    plot.redshift_visualization(slider.value, output)

def cobe_fit(bb_student_fn):
    """
    Creates an interactive plot for black body radiation with a slider to fit for the temperature.
    
    Parameters:
    - bb_student_fn: Student's implementation of the blackbody radiation.
    """
    
    def update_plot(temp):
        plot.cobe_curve_fit(temp, bb_student_fn)
        
    temp_slider = FloatSlider(
        value=5,
        min=1,
        max=10,
        step=0.1,
        description='Temp (K):',
        readout_format='.1f',
        tooltip='Temperature of the CMB'
    )
    
    interact(update_plot, temp=temp_slider)
