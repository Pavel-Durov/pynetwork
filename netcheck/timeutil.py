"""Utility script for time parsing/formating"""

import datetime

DATE_FORMAT = "%Y-%m-%d"
DATE_TIME_FORMAT = DATE_FORMAT + " %H:%M:%S"

def utc_now():
    """returns current utc time"""
    now = datetime.datetime.utcnow()
    return now

def  format_to_date_str(time):
    """Constructs and returns formatted date string, base on given timestamp"""
    return time.strftime(DATE_FORMAT)

def format_to_time_str(time):
    """Constructs and returns formatted time string, base on given timestamp"""
    return time.strftime(DATE_TIME_FORMAT)
