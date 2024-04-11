from typing import List, Callable, Optional
import numpy as np

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