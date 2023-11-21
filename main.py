import csv
import json
import custom_functions.time_functions as time_f
import custom_functions.input as input_f
from typing import List

ENROLLMENT_WINDOW_PATH: str = "data/enrollment_window.json"
LIST_ELEMENT: str = "> "
COURSE_LIST_PATH_TEMPLATE: str = "data/{quarter}/all_courses.txt"
FILE_NAME_TEMPLATE: str = "data/{quarter}/raw/{selected_class}.csv"
CSV_DELIMITER: str = ','
DATETIME_COL: int = 0
AVAILABLE_SEATS_COL: int = 2
STD_TIME: int = 12
DOUBLE_DIGITS: int = 10
ALL_CLASS_LEVELS_RELEASED: int = 1
ONE_CLASS_LEVEL: int = 2
WHICH_ENROLLMENT_PASS: int = 0
CLASS_LEVEL_1: int = 1
CLASS_LEVEL_2: int = 2
ALWAYS_SEATS_AVAILABLE_TEMPLATE: str = "{selected_class} always had seats available."

def format_output(
        quarter: str, 
        selected_class: str, 
        time: str, 
        enrollment_details: List[str]) -> str:
    """Formats output to be displayed to user."""

    if len(enrollment_details) == ALL_CLASS_LEVELS_RELEASED:
        # After all grades released
        pass # TODO

    # Class filled up during a singular class time slot
    elif len(enrollment_details) == ONE_CLASS_LEVEL:
        return "" \
            f"\n======================================================================\n"\
            f"{quarter} {selected_class} filled up at approximately {time} during {enrollment_details[WHICH_ENROLLMENT_PASS]}.\n"\
            f"This was during the timeslot for {enrollment_details[CLASS_LEVEL_1]}."\
            f"\n======================================================================\n"
    
    # Class filled up in between two class time slots
    else:
        return "" \
            f"\n======================================================================\n"\
            f"{quarter} {selected_class} filled up at approximately {time} during {enrollment_details[WHICH_ENROLLMENT_PASS]}.\n"\
            f"This was during the timeslot for {enrollment_details[CLASS_LEVEL_2]} and {enrollment_details[CLASS_LEVEL_1]}."\
            f"\n======================================================================\n"

def main():
    """Main method that executes all logic."""

    # Loads all of the enrollment windows by class standing
    with open(ENROLLMENT_WINDOW_PATH, 'r', encoding='utf8') as file:
        enrollment_window = json.load(file)

    while True:

        # Prompts what quarters user can choose
        for quarter in enrollment_window:
            print(LIST_ELEMENT + quarter)
        quarter = input_f.input_quarter(enrollment_window)
        if quarter is None:
            break

        # Loads all courses for given quarter
        all_courses_path = COURSE_LIST_PATH_TEMPLATE.format(quarter=quarter)
        with open(all_courses_path, 'r', encoding='utf8') as file:
            all_courses = file.read()
        all_courses_list = all_courses.split('\n')

        # Prompts user to select class
        selected_class = input_f.input_class(all_courses_list)
        if selected_class is None:
            break

        # Loads data for specific class
        file_name = FILE_NAME_TEMPLATE.format(quarter=quarter, selected_class=selected_class)
        csv_file = csv.reader(open(file_name, 'r', encoding='utf8'), delimiter=CSV_DELIMITER)

        first_row = True
        found_data = False
        for row in csv_file:
            
            # Skip header row
            if first_row:
                first_row = False
                continue

            # Skip if data is not within enrollment window
            if time_f.get_date_standard(row[DATETIME_COL]) not in enrollment_window[quarter]:
                continue

            if int(row[AVAILABLE_SEATS_COL]) == 0:

                found_data = True

                hour = time_f.get_hour(row[DATETIME_COL]) % STD_TIME
                am_pm = "AM"
                if time_f.get_hour(row[DATETIME_COL]) > STD_TIME:
                    am_pm = "PM"
                minute = time_f.get_minute(row[DATETIME_COL])
                time = f"{hour}:0{minute} {am_pm}" if minute < DOUBLE_DIGITS else f"{hour}:{minute} {am_pm}"
                print(format_output(quarter, selected_class, time,
                    enrollment_window[quarter][time_f.get_date_standard(row[DATETIME_COL])]))
                break
        if not found_data:
            print(ALWAYS_SEATS_AVAILABLE_TEMPLATE.format(selected_class=selected_class))

if __name__ == "__main__":
    main()
