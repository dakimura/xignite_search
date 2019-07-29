#-*- coding:utf-8 -*-
import datetime

def calc_last_open_date(date: datetime.date, closed_days) -> datetime.date:
    date = date - datetime.timedelta(days=1)

    # weekday: 5=Saturday, 6=Sunday
    while date in closed_days or date.weekday() == 5 or date.weekday() == 6:
        date = date - datetime.timedelta(days=1)

    return date
