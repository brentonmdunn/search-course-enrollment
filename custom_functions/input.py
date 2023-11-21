import re
from typing import Union

QTR_NOT_FOUND_MESSAGE = "Quarter not found."
QTR_INPUT_PROMPT = "Quarter (xx##): "
ISOLATE_DEPT_REGEX = r'[A-Za-z]+'
ISOLATE_COURSE_NUM_REGEX = r'(\d+)([A-Za-z]*)'

def user_quits(user_input: str) -> bool:
    """Quits application if detects a 'q' from user."""

    if user_input.lower() == 'q':
        return True
    return False

def input_quarter(enrollment_window) -> Union[str, None]:
    """
    Handles user input for quarter prompt.
    
    Returns quarter that user requested, None if fails.
    """

    first_qtr_req = True
    quarter_requested = None
    while quarter_requested is None:
        if not first_qtr_req:
            print(QTR_NOT_FOUND_MESSAGE)
        quarter_requested = input(QTR_INPUT_PROMPT)
        if user_quits(quarter_requested):
            return None
        quarter_requested = format_quarter(quarter_requested, enrollment_window)
        first_qtr_req = False
    return quarter_requested

def input_class(all_courses_list) -> Union[str, None]:
    """
    Handles user input for class prompt.
    
    Returns class that user requested, None if fails.
    """

    first_class_req = True
    selected_class = None
    while selected_class is None:
        if not first_class_req:

            """
            TODO: WIP--suggest similar courses
            # Isolate dept number
            isolate_dept_pattern = re.compile(ISOLATE_DEPT_REGEX)
            isolate_dept_obj = isolate_dept_pattern.search(selected_class_copy)
            dept = isolate_dept_obj.group(0)

            # Isolate couse number
            isolate_couse_num_pattern = re.compile(ISOLATE_COURSE_NUM_REGEX)
            isolate_course_num_obj = isolate_couse_num_pattern.search(
                selected_class_copy)
            course_num_whole = isolate_course_num_obj.group(0)          # Only number portion
            course_num_numbers_only = isolate_course_num_obj.group(1)   # Only letter portion

            custom_course_num_regex = dept + ' ' + \
                course_num_numbers_only + r"[A-Za-z]+"

            custom_course_num_pattern = re.compile(custom_course_num_regex)

            similar_classes = list(filter(custom_course_num_pattern.match, all_courses_list))

            print("Class not found. Similar classes: " + ', '.join(similar_classes))
            """
            print("Class not found. It may have not been offered.")
        selected_class = input("Class: ")
        if user_quits(selected_class):
            return None
        selected_class = format_class(selected_class, all_courses_list)
        first_class_req = False
    return selected_class


def format_quarter(raw, enrollment_window):
    """
    Standardizes output to have two capital letters followed by two numbers.
    
    Accepts input such as wi23, wi 23, WI23.

    Returns None if fails.
    """
    
    qtr_yr_regex = r"([A-Za-z]+)\s*(\d+)"      # Checks if contains letters followed by numbers
    qtr_yr = re.compile(qtr_yr_regex).search(raw)

    if not qtr_yr:
        return None

    qtr = qtr_yr.group(1).upper()
    yr = qtr_yr.group(2).upper()

    correct_format = qtr + yr

    if correct_format in enrollment_window:
        return correct_format
    
    return None

def format_class(raw, all_courses_list):
    class_regex = r"([A-Za-z]+)\s*(\d+)"
    selected_class = re.compile(class_regex).search(raw)

    if not selected_class:
        return None
    
    dept = selected_class.group(1).upper()
    number = selected_class.group(2).upper()

    correct_format = dept + " " + number

    if correct_format in all_courses_list:
        return correct_format

    return None
