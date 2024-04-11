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

