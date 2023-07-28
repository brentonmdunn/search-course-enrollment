import csv
import re


def get_year(time):
    return int(time[0:4])


def get_month(time):
    return int(time[5:7])


def get_day(time):
    return int(time[8:10])


def get_hour(time):
    return int(time[11:13])


def get_minute(time):
    return int(time[14:16])


def get_date_json(time):
    return {
        "year": get_year(time),
        "month": get_month(time),
        "day": get_day(time)
    }


def get_time_json(time):
    return {
        "hour": get_hour(time),
        "minute": get_minute(time)
    }


def get_date_standard(time):
    return time[:10]

# csv_file = csv.reader(open('data/FA22/MATH 20C.csv', 'r'), delimiter=',')


# Find when window closes
FA22 = {
    "2022-05-20": ["1st pass", "Priorities", "Seniors"],
    "2022-05-21": ["1st pass", "Seniors"],
    "2022-05-22": ["1st pass", "Seniors"],
    "2022-05-23": ["1st pass", "Seniors", "Juniors"],
    "2022-05-24": ["1st pass", "Juniors", "Sophomores"],
    "2022-05-25": ["1st pass", "Sophomores", "Freshmen"],
    "2022-05-28": ["2nd pass", "Priorities", "Seniors"],
    "2022-05-29": ["2nd pass", "Seniors"],
    "2022-05-30": ["2nd pass", "Seniors"],
    "2022-05-31": ["2nd pass", "Seniors", "Juniors"],
    "2022-06-01": ["2nd pass", "Juniors", "Sophomores"],
    "2022-06-02": ["2nd pass", "Sophomores", "Freshmen"]
}

view_options = ["1 - Run out of seats"]


quarter = input("Quarter (xx##): ")

all_courses_path = "data/" + quarter + "all_courses.txt"

with open(all_courses_path, 'r') as file:
    all_courses = file.read()
all_courses_list = all_courses.split('\n')


first_class_req = True
selected_class = ""
while selected_class not in all_courses_list:
    if not first_class_req:
        isolate_dept_regex = r"[A-Za-z]+"
        isolate_dept_pattern = re.compile(isolate_dept_regex)
        isolate_dept_obj = isolate_dept_pattern.search(selected_class)
        dept = isolate_dept_obj.group(0)
        isolate_course_num_regex = r"(\d+)([A-Za-z]*)"
        isolate_couse_num_pattern = re.compile(isolate_course_num_regex)
        isolate_course_num_obj = isolate_couse_num_pattern.search(
            selected_class)
        course_num_whole = isolate_course_num_obj.group(0)
        course_num_numbers_only = isolate_course_num_obj.group(1)

        custom_course_num_regex = dept + ' ' + \
            course_num_numbers_only + r"[A-Za-z]+"

        custom_course_num_pattern = re.compile(custom_course_num_regex)
        similar_classes = list(
            filter(custom_course_num_pattern.match, all_courses_list))

        print("Class not found. Similar classes: " + ', '.join(similar_classes))
    selected_class = input("Class: ")
    first_class_req = False

file_name = "data/" + quarter + "/raw/" + selected_class + ".csv"
csv_file = csv.reader(open(file_name, 'r'), delimiter=',')
input_type = input(
    "\n".join(view_options) + "\nEnter the data you would like to see: ")

first_row = True
found_data = False
if input_type == '1':
    for row in csv_file:
        if first_row:
            first_row = False
            continue
        if get_date_standard(row[0]) not in FA22:
            continue
        if int(row[2]) == 0:
            # print(row)
            # print(get_time_json(row[0]))
            found_data = True

            print("====================================")
            # print("This class filled up at approximately %d:%d",
            #       get_hour(row[0]) % 12, get_minute(row[0]))

            hour = get_hour(row[0]) % 12
            am_pm = "AM"
            if get_hour(row[0]) > 12:
                am_pm = "PM"
            minute = get_minute(row[0])
            if minute < 10:
                print(
                    f"This class filled up at approximately {hour}:0{minute} {am_pm}")
            else:
                print(
                    f"This class filled up at approximately {hour}:{minute} {am_pm}")
            print("This is during the time: " +
                  ', '.join(FA22[get_date_standard(row[0])]))
            break
    if not found_data:
        print("No data found.")
