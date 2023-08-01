import re

def input_quarter(enrollment_window):
    first_qtr_req = True
    quarter = None
    while quarter is None:
        if not first_qtr_req:
            print("Quarter not found.")
        quarter = input("Quarter (xx##): ")
        quarter = format_quarter(quarter, enrollment_window)
        first_qtr_req = False
    return quarter

def input_class(all_courses_list):
    first_class_req = True
    selected_class = None
    while selected_class is None:
        if not first_class_req:

            # Input: dept ##

            # Isolate dept number 
            isolate_dept_regex = r"[A-Za-z]+"
            isolate_dept_pattern = re.compile(isolate_dept_regex)
            isolate_dept_obj = isolate_dept_pattern.search(selected_class)
            dept = isolate_dept_obj.group(0)

            # Isolate couse number
            isolate_course_num_regex = r"(\d+)([A-Za-z]*)"
            isolate_couse_num_pattern = re.compile(isolate_course_num_regex)
            isolate_course_num_obj = isolate_couse_num_pattern.search(
                selected_class)
            course_num_whole = isolate_course_num_obj.group(0)          # Only number portion
            course_num_numbers_only = isolate_course_num_obj.group(1)   # Only letter portion

            custom_course_num_regex = dept + ' ' + \
                course_num_numbers_only + r"[A-Za-z]+"

            custom_course_num_pattern = re.compile(custom_course_num_regex)
            similar_classes = list(filter(custom_course_num_pattern.match, all_courses_list))

            print("Class not found. Similar classes: " + ', '.join(similar_classes))
        selected_class = input("Class: ")
        selected_class = format_class(selected_class, all_courses_list)
        first_class_req = False
    return selected_class


def format_quarter(raw, enrollment_window):
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


