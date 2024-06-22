import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style

def set_custom_layout(large: bool=False) -> None:
    plt.style.use(astropy_mpl_style)

    # Global settings for plots

    # Set global figure size
    plt.rcParams['figure.figsize'] = [16, 8]

    # Set the global default figure facecolor to white
    plt.rcParams['figure.facecolor'] = 'white'

    if large:
        # Set global font size
        plt.rcParams['font.size'] = 16
        plt.rcParams['axes.labelsize'] = 20
        plt.rcParams['xtick.labelsize'] = 20
        plt.rcParams['ytick.labelsize'] = 20

        # Set the default legend marker size globally
        plt.rcParams['legend.markerscale'] = 2

        # Increase title to plot distance
        plt.rcParams['axes.titley'] = 1.05

    # Set the color cycle to include 10 easily distinguishable colors
    plt.style.use('tableau-colorblind10')