import numpy as np
from . import blackbody, tester

def test_blackbody_radiation_law(student_func):
    """
    Tests the student's implementation of the black body radiation law function.
    
    Parameters:
    - student_func: The student's function to test.
    
    Returns:
    - String with feedback based on the test results.
    """
    
    # Test cases
    test_cases = [
        ("Visible light, approx. sun's surface temp", (500e-9, 5778)),
        ("Microwave, approx. CMB temp", (1e-3, 2.725)),
    ]

    def formatter(case, expected, result):
        scenario, (wavelength, temp) = case
        return(f"Scenario {scenario} failed:\nWavelength={wavelength} m and temperature={temp} K.\n" +
                                    f"Expected result was close to {expected:.2e} W/m^2/sr/m, but got {result:.2e}.")

    return tester.create_test_cases('Blackbody Radiation', test_cases,
                                    blackbody.radiation_law_wavelength, student_func, formatter)


def test_peak_wavelength(student_func):
    """
    Tests the student's implementation for calculating the peak wavelength of black body
    radiation for a given temperature using Wien's Law.
    
    Parameters:
    - student_func: The student's function to test.
    
    Returns:
    - String with feedback based on the test results.
    """
    
    test_cases = [
        ("Sun's surface temperature", (5778, )),  # The Sun's surface temp in Kelvin
        ("Sirius Star temperature", (9940, )),    # Temperature of Sirius, a bright star
        ("Cool red star", (3000, )),              # Approximate temp of a cool red star
        ("Incandescent light bulb", (2400, )),    # Common temp for an old light bulb
        ("Hot blue star", (20000, )),             # High temp typical of a hot blue star
    ]

    def formatter(case, expected, result):
        scenario, (temp, ) = case
        return(f"Scenario {scenario} failed:\nTemperature={temp} K.\n" +
            f"Expected peak wavelength was close to {expected:.2e} m, but got {result:.2e} m.")


    return tester.create_test_cases("Wien's Law", test_cases,
                                    blackbody.peak_wavelength, student_func, formatter)

