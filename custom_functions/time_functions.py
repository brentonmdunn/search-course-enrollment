"""Date time getter methods given date time ISO 8601 format."""

from typing import Dict


YR_START_IDX: int = 0
YR_END_IDX: int = 4
MONTH_START_IDX: int = 5
MONTH_END_IDX: int = 7
DAY_START_IDX: int = 8
DAY_END_IDX: int = 10
HR_START_IDX: int = 11
HR_END_IDX: int = 13
MIN_START_IDX: int = 14
MIN_END_IDX: int = 16
DATE_START_IDX: int = 0
DATE_END_IDX: int = 10


def get_year(time: str) -> int:
    """Returns year given data time ISO 8601 format."""
    return int(time[YR_START_IDX : YR_END_IDX])


def get_month(time: str) -> int:
    """Returns month given data time ISO 8601 format."""
    return int(time[MONTH_START_IDX : MONTH_END_IDX])


def get_day(time: str) -> int:
    """Returns day given data time ISO 8601 format."""
    return int(time[DAY_START_IDX : DAY_END_IDX])


def get_hour(time: str) -> int:
    """Returns hour given data time ISO 8601 format."""
    return int(time[HR_START_IDX : HR_END_IDX])


def get_minute(time: str) -> int:
    """Returns minute given data time ISO 8601 format."""
    return int(time[MIN_START_IDX : MIN_END_IDX])


def get_date_json(time: str) -> Dict[str, int]:
    """Returns date given data time ISO 8601 format."""
    return {
        "year": get_year(time),
        "month": get_month(time),
        "day": get_day(time)
    }


def get_time_json(time: str) -> Dict[str, int]:
    """Returns time given data time ISO 8601 format."""
    return {
        "hour": get_hour(time),
        "minute": get_minute(time)
    }


def get_date_standard(time: str) -> str:
    """Returns date given data time ISO 8601 format."""
    return time[DATE_START_IDX : DATE_END_IDX]
