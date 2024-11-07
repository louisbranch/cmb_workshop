from typing import List, Callable, Optional
import numpy as np
from . import functions
from .i18n import I18N

i18n = I18N()

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
                return i18n.gettext("test_not_implemented").format(name)
            
            if not np.isclose(result, expected, rtol=1e-5, atol=0):
                raise ValueError
            
        except ValueError:
            if message_formatter is None:
                msg = i18n.gettext("scenario_failed").format(scenario, expected, result)
            else:
                msg = message_formatter(case, expected, result)
            messages.append(msg)
    
    if not messages:
        return i18n.gettext("all_tests_passed")
    else:
        return "\n\n".join(messages)

def test_blackbody_radiation(student_func):
    """
    Tests the student's implementation of the black body radiation law function.
    
    Parameters:
    - student_func: The student's function to test.
    
    Returns:
    - String with feedback based on the test results.
    """
    
    # Test cases
    test_cases = [
        (i18n.gettext("visible_light_scenario"), (500e-9, 5778)),
        (i18n.gettext("microwave_scenario"), (1e-3, 2.725)),
    ]

    def formatter(case, expected, result):
        scenario, (wavelength, temp) = case
        return (
            i18n.gettext("scenario_failed_message").format(
                scenario, wavelength, temp, expected, result
            )
        )

    return create_test_cases(
        i18n.gettext("test_blackbody_radiation_name"), 
        test_cases,
        functions.blackbody_radiation, 
        student_func, 
        formatter
    )

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
        (i18n.gettext("sun_surface_temp"), (5778, )),
        (i18n.gettext("sirius_temp"), (9940, )),
        (i18n.gettext("cool_red_star"), (3000, )),
        (i18n.gettext("incandescent_bulb"), (2400, )),
        (i18n.gettext("hot_blue_star"), (20000, )),
    ]

    def formatter(case, expected, result):
        scenario, (temp,) = case
        return (
            i18n.gettext("scenario_failed_wavelength").format(
                scenario, temp, expected, result
            )
        )

    return create_test_cases(
        i18n.gettext("test_wien_law_name"),
        test_cases,
        functions.peak_wavelength,
        student_func,
        formatter
    )