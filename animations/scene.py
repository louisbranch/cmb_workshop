from manim import *

class DopplerEffect(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_freq = None  # Initialize last_freq to store the last frequency

    def construct(self):
        title = Text('Blueshift', font_size=36)
        title.to_edge(UP)
        self.add(title)

        # Initialize a ValueTracker for frequency, starting at 1 Hz and increasing
        frequency = ValueTracker(0.1)

        # Initialize a ValueTracker for x-axis shift
        x_shift = ValueTracker(-5)  # Start from the left of the screen

        # Create source emitter, updating their position using always_redraw
        source = always_redraw(lambda: self.get_dot_with_label(x_shift.get_value()))

        obs = Dot(color=ORANGE).move_to([6, 0, 0])
        obs_label = Text("Observer", font_size=24).next_to(obs, DOWN)
        observer = VGroup(obs, obs_label)

        # Create a sine wave that dynamically updates based on the frequency, x_shift, and color
        sine_wave = always_redraw(lambda: self.get_sine_wave(
            frequency.get_value(),
            x_shift.get_value(),
            self.color_interpolation(frequency.get_value())
        ))

        # Add the sine wave to the scene
        self.add(title, source, observer, sine_wave)

        # Blueshift
        self.play(
            frequency.animate.set_value(10),
            x_shift.animate.set_value(0),  # Move to the right of the screen
            run_time=5,
            rate_func=linear
        )

        self.wait(2)

        self.remove(title)
        title = Text('Redshift', font_size=36)
        title.to_edge(UP)
        self.add(title)

        # Redshift
        self.play(
            frequency.animate.set_value(1),
            x_shift.animate.set_value(-5),  # Move to the left of the screen
            run_time=5,
            rate_func=linear
        )

        # Keep the scene displayed after the animation
        self.wait()
    
    def get_dot_with_label(self, x_shift):
        # Create a dot at the current x position
        dot = Dot(color=YELLOW).move_to([x_shift, 0, 0])
        # Create a text label and position it under the dot
        label = Text("Source", font_size=24).next_to(dot, LEFT)
        # Group the dot and the label together so they move as one unit
        return VGroup(dot, label)

    def get_sine_wave(self, freq, shift, color):
        # Define the parametric function for the sine wave with horizontal shift and dynamic color
        def parametric_sine_wave(t):
            k = 0.01 # rate of increase

            # x value will be t plus the horizontal shift, y is the sine of the frequency plus increase
            return np.array([t + shift, np.sin(np.pi * freq * t + np.pi * k * t**2), 0])

        # Create the ParametricFunction using the defined function with dynamic coloring
        return ParametricFunction(
            parametric_sine_wave,
            t_range=[0, 5, 0.01],
            color=color
        )

    def color_interpolation(self, current_freq):
        if self.last_freq is None or current_freq == self.last_freq:
            direction = 0
        elif current_freq > self.last_freq:
            direction = 1
        else:
            direction = -1 

        self.last_freq = current_freq  # Update last_freq for the next call

        # Set base color to white
        base_color = WHITE

        # Define the max and min frequency values for full color change
        max_freq = 10  # Define the frequency at which the color becomes fully blue
        min_freq = 8   # Define the frequency at which the color starts to become fully red

        # Calculate ratio based on the direction of the frequency change
        if direction == 1:  # Frequency is increasing
            ratio = (current_freq - 1) / (max_freq - 1)
            return interpolate_color(base_color, PURE_BLUE, ratio)
        elif direction == -1:  # Frequency is decreasing
            ratio = (current_freq - min_freq) / (1 - min_freq)
            return interpolate_color(base_color, PURE_RED, ratio)
        else:
            return base_color