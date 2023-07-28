import csv


def get_year(time):
    return time[0:4]


def get_month(time):
    return time[5:7]


def get_day(time):
    return time[8:10]


def get_hour(time):
    return time[11:13]


def get_minute(time):
    return time[14:16]


def get_date(time):
    return {
        "year": get_year(time),
        "month": get_month(time),
        "day": get_day(time)
    }


def get_time(time):
    return {
        "hour": get_hour(time),
        "minute": get_minute(time)
    }


# csv_file = csv.reader(open('data/FA22/MATH 20C.csv', 'r'), delimiter=',')

# first_row = True
# for row in csv_file:
#     if first_row:
#         first_row = False
#         continue
#     if int(row[3]) > 0:
#         print(row)
#         print(get_time(row[0]))
#         break


selected_class = input("Class: ")
quarter = input("Quarter (xx##): ")
file_name = "data/" + quarter + "/" + selected_class + ".csv"
csv_file = csv.reader(open(file_name, 'r'), delimiter=',')
input_type = input(
    "e = zero seats left\nEnter the data you would like to see: ")

first_row = True
found_data = False
if input_type == 'e':
    for row in csv_file:
        if first_row:
            first_row = False
            continue
        if int(row[2]) == 0:
            print(row)
            print(get_time(row[0]))
            found_data = True
            break
    if not found_data:
        print("No data found.")
