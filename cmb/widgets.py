import numpy as np
from ipywidgets import interact, Output, Label, VBox, HBox, widgets
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
    
    def update(temp, ref):
        ref_name, ref_temp = ref
        plot.peak_wavelength(wavelengths, ref_name, ref_temp, temp, bb_student_fn, wl_student_fn)

    temperature = temperature_slider()
    reference = reference_dropdown()
    set_widget_styles([temperature, reference])
    
    interact(update, temp=temperature, ref=reference)

def blackbody_radiation(student_fn, wavelengths=const.wavelengths):
    """
    Creates an interactive plot for black body radiation with a slider to adjust the temperature.
    
    Parameters:
    - student_fn: Student's implementation of the black body radiation law.
    - wavelengths: Array of wavelengths (in meters) to plot.
    """
    
    def update(temp, ref):
        ref_name, ref_temp = ref
        plot.blackbody_radiation(wavelengths, ref_name, ref_temp, temp, student_fn)
        
    temperature = temperature_slider()
    reference = reference_dropdown()
    set_widget_styles([temperature, reference])
    
    interact(update, temp=temperature, ref=reference)

def redshift():
    output = Output()

    slider = widgets.FloatSlider(
        value=0,
        min=-8e7,
        max=1e8,
        step=1e6,
        description='Velocity (m/s):',
        readout=False,
        tootltip='Velocity of the galaxy.'
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
    set_widget_styles([slider, velocity_label])

    display(ui)

    plot.redshift_visualization(slider.value, output)

def cobe_fit(bb_student_fn):

    temperature_references = {
        'Human Body': (290, 310),
        'Dry Ice': (190, 210),
        'Liquid Nitrogen': (90, 110),
        'Cryogenic Freezer': (5, 15),
        'Superconductor Exp.': (0, 5)
    }

    reference_selector = widgets.SelectionSlider(
        options=list(temperature_references.keys()),
        value='Human Body',
        description='As hot/cold as:',
        continuous_update=False
    )

    temperature_slider = widgets.FloatSlider(
        value=(290 + 310) / 2,
        min=290,
        max=310,
        step=(310 - 290) / 100,
        description='Temperature (K):',
        continuous_update=False,
        tooltip='Temperature of the CMB'
    )

    # Update the temperature slider range based on the selected magnitude
    def update_temperature_slider(*args):
        reference = reference_selector.value
        min_temp, max_temp = temperature_references[reference]

        with temperature_slider.hold_sync(), temperature_slider.hold_trait_notifications():
            temperature_slider.min = min_temp
            temperature_slider.max = max_temp
            temperature_slider.value = (min_temp + max_temp) / 2
            temperature_slider.step = (max_temp - min_temp) / 100

    reference_selector.observe(update_temperature_slider, names='value')

    set_widget_styles([reference_selector, temperature_slider])
    display(reference_selector, temperature_slider)

    output = widgets.Output()

    def update_plot(*args):
        plot.cobe_curve_fit(temperature_slider.value, bb_student_fn, output)

    # Link the display function to changes in the temperature slider
    temperature_slider.observe(update_plot, names='value')

    update_plot()
    display(output)

def reference_dropdown():
    return widgets.Dropdown(
        options=[(name, (name, temp)) for name, temp in const.reference_objects],
        value=("Sun", 5778),  # Default value
        description='Reference Object:',
        tooltip='Reference object to compare with.'
    )

def temperature_slider(value=5778):
    return widgets.FloatSlider(
        value=value,
        min=1000,
        max=10000,
        step=100,
        description='Temperature (K):',
        readout_format='.0f',
        tooltip='Temperature of the black body.'
    )

def set_widget_styles(list, description_width='initial'):
    for widget in list:
        if isinstance(widget, widgets.HBox):
            for w in widget.children:
                w.style.description_width = description_width
                w.layout.width = '40%'
        else:
            widget.style.description_width = description_width
            widget.layout.width = '45%'