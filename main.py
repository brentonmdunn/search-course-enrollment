import csv
import re
import json
import time_functions as time_f

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
    selected_class = ""
    while selected_class not in all_courses_list:
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
            similar_classes = list(
                filter(custom_course_num_pattern.match, all_courses_list))

            print("Class not found. Similar classes: " + ', '.join(similar_classes))
        selected_class = input("Class: ")
        first_class_req = False


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


def format_output(quarter, selected_class, time, enrollment_details):

    if len(enrollment_details) == 1:
        # After all grades released
        pass
    elif len(enrollment_details) == 2:
        return "" \
            f"\n======================================================================\n"\
            f"{quarter} {selected_class} filled up at approximately {time} during {enrollment_details[0]}.\n"\
            f"This was during the timeslot for {enrollment_details[1]}."\
            f"\n======================================================================\n"
    else:
        return "" \
            f"\n======================================================================\n"\
            f"{quarter} {selected_class} filled up at approximately {time} during {enrollment_details[0]}.\n"\
            f"This was during the timeslot for {enrollment_details[2]} and {enrollment_details[1]}."\
            f"\n======================================================================\n"


with open("enrollment_window.json", 'r') as file:
    enrollment_window = json.load(file)

quarter = input_quarter(enrollment_window)
all_courses_path = "data/" + quarter + "/all_courses.txt"

with open(all_courses_path, 'r') as file:
    all_courses = file.read()
all_courses_list = all_courses.split('\n')

selected_class = input_class(all_courses_list)
file_name = "data/" + quarter + "/raw/" + selected_class + ".csv"
csv_file = csv.reader(open(file_name, 'r'), delimiter=',')

first_row = True
found_data = False
for row in csv_file:
    if first_row:
        first_row = False
        continue
    if time_f.get_date_standard(row[0]) not in enrollment_window[quarter]:
        continue
    if int(row[2]) == 0:

        found_data = True

        hour = time_f.get_hour(row[0]) % 12
        am_pm = "AM"
        if time_f.get_hour(row[0]) > 12:
            am_pm = "PM"
        minute = time_f.get_minute(row[0])
        time = f"{hour}:0{minute} {am_pm}" if minute < 10 else f"{hour}:{minute} {am_pm}"
        print(format_output(quarter, selected_class, time,
              enrollment_window[quarter][time_f.get_date_standard(row[0])]))
        break
if not found_data:
    print(f"{selected_class} always had seats available.")
