from datetime import date

MONTH_LABELS = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
]
DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class NotValidDateError(Exception):
    pass


def validate_date(year, month, day=1):
    try:
        input_date = date(int(year), int(month), int(day))
    except (TypeError, ValueError):
        raise NotValidDateError

    if input_date < date(1970, 1, 1) or input_date > date.today():
        raise NotValidDateError

    return input_date



def get_calendar_data(year, month):
    if month not in range(1, 13):
        raise Exception('Invalid Month')

    month_label = MONTH_LABELS[month - 1]
    first_day = date(year, month, 1).weekday()
    month_length = DAYS_IN_MONTH[month - 1]
    if month == 2 and year % 4 == 0 and year % 100 != 0 and year % 400 == 0:
        month_length = 29

    month_list = []
    for i in range(first_day):
        month_list.append('')
    month_list += range(1, month_length + 1)
    return month_label, month_list
