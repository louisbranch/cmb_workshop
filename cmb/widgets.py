import math
import os
import uuid
from dataclasses import dataclass
from typing import List

import numpy as np
from ipywidgets import interact, Output, Label, VBox, HBox, widgets
from IPython.display import display, IFrame

from . import plot, const, cmb_utils

@dataclass
class CMBStoringData:
    map: object
    coords: List[List[float]]
    mean_image: object

    def __init__(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        fits=f'{dir}/../data/COM_CMB_IQU-commander_1024_R2.02_dg16_car.fits'
        self.map = cmb_utils.load_cmb_map(fits)
        self.coords = const.cmb_thumbnails_coords
        self.mean_image = None

# global instance to store the data accross the widgets
cmb_data = CMBStoringData()

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

    output = Output()
    
    def update(temp, ref):
        ref_name, ref_temp = ref
        with output:
            output.clear_output(wait=True)
            plot.blackbody_radiation(wavelengths, ref_name, ref_temp, temp, student_fn)
        
    temperature = temperature_slider()
    reference = reference_dropdown()
    set_widget_styles([temperature, reference])
    
    interact(update, temp=temperature, ref=reference)
    display(output)

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
        'Superconductor': (0, 5)
    }

    reference_selector = widgets.SelectionSlider(
        options=list(temperature_references.keys()),
        value='Human Body',
        description='Temperature Reference (from hot to cold):',
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

    set_widget_styles([reference_selector], width=60)
    set_widget_styles([temperature_slider])
    display(reference_selector, temperature_slider)

    output = widgets.Output()

    def update_plot(*args):
        plot.cobe_curve_fit(temperature_slider.value, bb_student_fn, output)

    # Link the display function to changes in the temperature slider
    temperature_slider.observe(update_plot, names='value')

    update_plot()
    display(output)

def cmb_std_dev():

    guidelines = widgets.Checkbox(
        value=False,
        description='Show Guidelines',
        disabled=False,
        tooltip='Show guidelines for the standard deviation.',
        indent=False
    )

    def update_plot(guidelines):
        map = cmb_data.map
        if map is not None:
            plot.cmb_std_dev(map, guidelines)

    interact(update_plot, guidelines=guidelines)


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

def cmb_planck_map():
    plot.planck_map(cmb_data.map)

def cmb_map_iframe(height=400):
    display(IFrame(const.cmb_map_url, width='100%', height=f'{height}px'))

def cmb_map_objects(num_cols=3, path='media'):

    #TODO: combine i18n and media paths
    image_paths = [
        f'{path}/cmb_spot_1.png',
        f'{path}/cmb_spot_2.png',
        f'{path}/cmb_spot_3.png',
        f'{path}/cmb_spot_4.png',
        f'{path}/cmb_spot_5.png',
    ]

    def read_image(image_path):
        with open(image_path, "rb") as image_file:
            return image_file.read()

    object_types = ['Hot Spot', 'Cold Spot', 'Star', 'Galaxy', 'Galaxy Cluster', 'Milky Way Galaxy']
    correct_answers = ['Galaxy Cluster', 'Galaxy', 'Galaxy Cluster', 'Star', 'Milky Way Galaxy']

    dropdowns = [
        widgets.Dropdown(
            options=object_types,
            description='Type:',
            layout=widgets.Layout(width='auto')
        )
        for _ in image_paths
    ]
    image_widgets = [
        widgets.Image(
            value=read_image(image),
            format='png',
            width=200
        )
        for image in image_paths
    ]

    num_images = len(image_paths)
    num_rows = math.ceil(num_images / num_cols)

    grid = widgets.GridspecLayout(num_rows, num_cols, height='auto')

    #FIXME improve grid layout
    for i in range(num_rows):
        for j in range(num_cols):
            idx = i * num_cols + j
            if idx < num_images:
                box = widgets.VBox([image_widgets[idx], dropdowns[idx]])
                grid[i, j] = box

    result_label = widgets.Label()

    # TODO: find a better way to style the answers
    def check_answers(b):
        correct_count = 0

        for i, dropdown in enumerate(dropdowns):
            if dropdown.value == correct_answers[i]:
                dropdown.layout.border = '2px solid lightgreen'
                correct_count += 1
            else:
                dropdown.layout.border = '2px solid lightcoral'
        
        if correct_count == num_images:
            result_label.value = "You've mastered it! All answers are correct!"
        else:
            result_label.value = f"You got {correct_count} out of {num_images} correct."

    check_button = widgets.Button(description='Check Answers')
    check_button.on_click(check_answers)
    center([result_label, check_button])

    display(grid)
    display(widgets.VBox([widgets.Box([check_button], layout=centered()), result_label]))

def calculate_moon_distance(moon_distance=0, light_time=0):
    expected_distance_m = (const.moon_r * 2) / const.moon_angular_size
    expected_time_for_light_s = expected_distance_m / const.c

    distance_input = widgets.FloatText(description='Distance to the Moon (km):', value=moon_distance)
    time_input = widgets.FloatText(description='Light Travel Time (s):', value=light_time)
    check_button = widgets.Button(description='Check Answers')
    result_output = widgets.Label()

    set_widget_styles([distance_input, time_input], width=30)

    # Function to check and display the results
    def check_answers(b):
        user_distance = distance_input.value
        user_time = time_input.value
        
        distance_tolerance = 1e3
        time_tolerance = 0.05
        
        distance_delta = abs(user_distance - expected_distance_m/1e3)
        time_delta = abs(user_time - expected_time_for_light_s)

        messages = []

        if distance_delta < distance_tolerance and time_delta < time_tolerance:
            messages.append("Correct! Your calculations are within the expected range.")
        elif distance_delta < distance_tolerance and time_delta >= time_tolerance:
            messages.append("Your distance is calculation correct!")
            messages.append("Check your time calculation. Rembember to convert units where necessary (speed of light is given in m/s).")
        else:
            messages.append("Check your calculations.")
            messages.append("Remember to convert units where necessary (angular diameter needs to be in radians).")

        result_output.value = '\n'.join(messages)

    check_button.on_click(check_answers)

    display(widgets.VBox([distance_input, time_input, check_button, result_output]))

def coordinate_inputs():

    output = Output()
    container = widgets.VBox()
    coord_widgets = []

    def update(change=None):
        coords = []
        for i, (lat_input, long_input, id) in enumerate(coord_widgets):
            lat, long = lat_input.value, long_input.value
            if lat is not None and long is not None:
                coords.append((lat_input.value, long_input.value))
        
        cmb_data.coords = coords

        thumbnails = cmb_utils.extract_thumbnails(cmb_data.map, coords)
        with output:
            output.clear_output(wait=True)
            cmb_utils.plot_thumbnails(thumbnails, figsize=(10, 6))

    def on_remove_button_clicked(change):
        for child in container.children:
            if child.id == change.id:
                container.children = tuple([child for child in container.children if child.id != change.id])
                update()
        for lat_input, long_input, id in coord_widgets:
            if id == change.id:
                coord_widgets.remove((lat_input, long_input, id))
                break

        update()

    def add_coordinate_inputs(lat=None, long=None):
        index_label = widgets.Label(
            value=f'Coordinate {(len(coord_widgets) + 1):2}:'.replace(' ', '\xa0')
        )
        lat_input = widgets.FloatText(
            value=lat,
            description='Lat (deg):',
            step=0.0001,
            continuous_update=True,
            tooltip='Latitude in degrees.'
        )
        long_input = widgets.FloatText(
            value=long,
            description='Long (deg):',
            step=0.0001,
            continuous_update=True,
            tooltip='Longitude in degrees.'
        )

        id = uuid.uuid4()

        remove = widgets.Button(description='Remove')
        remove.id = id

        coord_widgets.append((lat_input, long_input, id))
        box = widgets.HBox([index_label, lat_input, long_input, remove])
        box.id = id

        lat_input.observe(update, names='value')
        long_input.observe(update, names='value')
        remove.on_click(on_remove_button_clicked)

        container.children += (box,)
    
    for lat, long in cmb_data.coords:
        add_coordinate_inputs(lat, long)
    
    add_button = widgets.Button(description='Add Coordinates')
    
    def on_add_button_clicked(b):
        add_coordinate_inputs()
        update()

    add_button.on_click(on_add_button_clicked)
    
    update()
    display(container, add_button, output)

def cmb_thumbnails_averaging():

    output = Output()

    slider = widgets.IntSlider(
        value=1,
        min=1,
        max=len(cmb_data.coords),
        step=1,
        description='Number of thumbnails:',
        readout=True,
        continuous_update=False,
        tooltip='Number of thumbnails to average.'
    )

    def update(amount):
        thumbnails = cmb_utils.extract_thumbnails(cmb_data.map, cmb_data.coords[0:amount])
        mean_thumbnail = np.mean(thumbnails, axis=0)
        with output:
            output.clear_output(wait=True)
            plot.view_map_pixel(mean_thumbnail)
        cmb_data.mean_image = mean_thumbnail

    set_widget_styles([slider]) 

    interact(update, amount=slider)
    display(output)

def averaged_hotspot_profile(plot_fn, img_fn):

    slider = widgets.IntSlider(
        value=20,
        min=20,
        max=95,
        step=1,
        description='Peak Threshold:',
        readout=False,
        tooltip='Threshold for peak detection.'
    )
    percent = widgets.Label(value=f'{slider.value}%')

    set_widget_styles([slider, percent])

    graph = Output()
    img = Output()

    def on_change(change):
        percent.value = f'{change["new"]}%'
        update()

    def update():
        if cmb_data.mean_image is None:
            with graph:
                graph.clear_output(wait=True)
                label = widgets.Label(value='No data available. Please check your average hotspot image.')
                display(label)
                return

        with graph:
            graph.clear_output(wait=True)
            threshold = slider.value / 100
            shape = plot_fn(cmb_data.mean_image, threshold)
        with img:
            img.clear_output(wait=True)
            img_fn(cmb_data.mean_image, shape)

    slider.observe(on_change, names='value')

    update()
    display(widgets.HBox([slider, percent]))

    # Wrap the buttons in a VBox to center them vertically
    vbox1 = widgets.VBox([graph], layout=widgets.Layout(justify_content='center'))
    vbox2 = widgets.VBox([img], layout=widgets.Layout(justify_content='center'))

    # Create an HBox to arrange the VBox elements horizontally
    hbox = widgets.HBox([vbox1, vbox2], layout=widgets.Layout(align_items='center'))
    display(hbox)

def averaged_hotspot_horizontal_profile():
    averaged_hotspot_profile(plot.averaged_hotspot_horizontal_profile, plot.view_map_pixel)

def averaged_hotspot_radial_profile():
    averaged_hotspot_profile(plot.averaged_hotspot_radial_profile, plot.view_map_degrees)

def set_widget_styles(list, description_width='initial', width=45):
    for widget in list:
        if isinstance(widget, widgets.HBox):
            for w in widget.children:
                w.style.description_width = description_width
                w.layout.width = '40%'
        else:
            widget.style.description_width = description_width
            widget.layout.width = f'{width}%'

def centered():
    return widgets.Layout(margin='10px 0 0 0', display='flex', justify_content='center')

def center(list):
    for widget in list:
        widget.layout = centered()