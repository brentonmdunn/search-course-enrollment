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
