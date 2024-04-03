import numpy as np
from . import blackbody

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
        (500e-9, 5778, "Visible light, approx. sun's surface temp"),
        (1e-3, 2.725,  "Microwave, approx. CMB temp"),
    ]

    feedback_messages = []
    
    for wavelength, temp, scenario in test_cases:
        expected = blackbody.radiation_law_wavelength(wavelength, temp)
        try:
            result = student_func(wavelength, temp)
            if result is None:
                return "Blackbody radiation function not implemented. Skipping tests."
            
            # Custom check for closeness instead of assert_allclose
            if not np.isclose(result, expected, rtol=1e-5, atol=0):
                raise ValueError
            
        except ValueError:
            feedback_messages.append(f"Scenario {scenario} failed:\nWavelength={wavelength} m and temperature={temp} K.\n" +
                                     f"Expected result was close to {expected:.2e} W/m^2/sr/m, but got {result:.2e}.")
    
    if not feedback_messages:  # If the list is empty, all tests passed
        return "All tests passed! Your implementation appears to be correct."
    else:
        return "\n\n".join(feedback_messages)  # Join all feedback messages into a single string