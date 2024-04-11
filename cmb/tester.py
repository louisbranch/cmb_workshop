from typing import List, Callable, Optional
import numpy as np
from . import functions

def create_test_cases(name: str, test_cases: List,
                      original_func: Callable, student_func: Callable,
                      message_formatter: Optional[Callable] = None):
    """
    Tests a student's function against an original function using a set of test cases. 
    It evaluates whether the student's function behaves as expected by comparing its output 
    with the original function's output for the same arguments. If discrepancies occur,
    formatted error messages are generated. The function can optionally use a custom 
    message formatter for error messages.

    Parameters:
    - name (str): Name for the test suite, used for identifying the test cases.
    - test_cases (List[Tuple[str, List]]): A list of test case tuples, each containing a scenario description and a list of arguments.
    - original_func (Callable): The reference function to produce the correct output for the provided arguments.
    - student_func (Callable): The student's function to be tested against the original function.
    - message_formatter (Optional[Callable]): An optional function to format error messages, accepts the test case, expected result, and actual result.

    Returns:
    - str: A single string indicating all tests passed, or concatenated error messages for each failing test case.
          If the student function is not implemented, it returns a message indicating this and skips the tests.
    """
    messages = []
    
    for case in test_cases:
        scenario, args = case
        expected = original_func(*args)
        try:
            result = student_func(*args)
            if result is None:
                return f"{name} function not implemented. Skipping tests."
            
            if not np.isclose(result, expected, rtol=1e-5, atol=0):
                raise ValueError
            
        except ValueError:
            if message_formatter is None:
                msg = f"Scenario {scenario} failed. Expected result was close to {expected:.2e}, but got {result:.2e}."
            else:
                msg = message_formatter(case, expected, result)
            messages.append(msg)
    
    if not messages:
        return "All tests passed! Your implementation appears to be correct."
    else:
        return "\n\n".join(messages)

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

    return create_test_cases('Blackbody Radiation', test_cases,
                                    functions.radiation_law_wavelength, student_func, formatter)


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


    return create_test_cases("Wien's Law", test_cases,
                                    functions.peak_wavelength, student_func, formatter)
