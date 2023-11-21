"""Handles input for program."""

import re
from typing import List, Optional, Match

QTR_NOT_FOUND_MESSAGE: str = "Quarter not found."
QTR_INPUT_PROMPT: str = "Quarter (xx##): "
ISOLATE_DEPT_REGEX: str = r'[A-Za-z]+'
ISOLATE_COURSE_NUM_REGEX: str = r'(\d+)([A-Za-z]*)'
QTR_YR_REGEX: str = r"([A-Za-z]+)\s*(\d+)"      # Checks if contains letters followed by numbers
CLASS_REGEX: str = r'([A-Za-z]+)\s*(\d+)'
QUIT_CHAR: str = 'q'

def user_quits(user_input: str) -> bool:
    """Quits application if detects a 'q' from user."""

    if user_input.lower() == QUIT_CHAR:
        return True
    return False

def input_quarter(enrollment_window: List[str]) -> Optional[str]:
    """
    Handles user input for quarter prompt.
    
    Returns quarter that user requested, None if fails.
    """

    first_qtr_req: bool = True
    quarter_requested: bool = None
    while quarter_requested is None:
        if not first_qtr_req:
            print(QTR_NOT_FOUND_MESSAGE)
        quarter_requested = input(QTR_INPUT_PROMPT)
        if user_quits(quarter_requested):
            return None
        quarter_requested: Optional[str] = format_quarter(quarter_requested, enrollment_window)
        first_qtr_req = False
    return quarter_requested

def input_class(all_courses_list: List[str]) -> Optional[str]:
    """
    Handles user input for class prompt.
    
    Returns class that user requested, None if fails.
    """

    first_class_req: bool = True
    selected_class: Optional[str] = None
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


def format_quarter(raw: str, enrollment_window: List[str]) -> Optional[str]:
    """
    Standardizes output to have two capital letters followed by two numbers.
    
    Accepts input such as wi23, wi 23, WI23.

    Returns None if fails.
    """
    
    qtr_yr: Optional[Match] = re.compile(QTR_YR_REGEX).search(raw)

    if not qtr_yr:
        return None

    qtr: Optional[str] = qtr_yr.group(1).upper()
    yr: Optional[str] = qtr_yr.group(2).upper()

    correct_format: str = qtr + yr

    if correct_format in enrollment_window:
        return correct_format
    
    return None

def format_class(raw: str, all_courses_list: List[str]) -> Optional[str]:
    """Standardizes class format."""
    
    selected_class: Optional[Match] = re.compile(CLASS_REGEX).search(raw)

    if not selected_class:
        return None
    
    dept: Optional[str] = selected_class.group(1).upper()
    number: Optional[str] = selected_class.group(2).upper()

    correct_format: str = dept + " " + number

    if correct_format in all_courses_list:
        return correct_format

    return None
