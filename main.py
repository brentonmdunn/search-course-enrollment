import csv
import json
import custom_functions.time_functions as time_f
import custom_functions.input as input_f

ENROLLMENT_WINDOW_PATH: str = "enrollment_window.json"
LIST_ELEMENT: str = "> "
COURSE_LIST_PATH_TEMPLATE = "data/{quarter}/all_courses.txt"

def format_output(quarter, selected_class, time, enrollment_details):

    if len(enrollment_details) == 1:
        # After all grades released
        pass # TODO
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

        file_name = "data/" + quarter + "/raw/" + selected_class + ".csv"
        csv_file = csv.reader(open(file_name, 'r', encoding='utf8'), delimiter=',')

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

if __name__ == "__main__":
    main()
