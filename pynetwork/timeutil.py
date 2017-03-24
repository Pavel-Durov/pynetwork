"""Utility script for time parsing/formating"""

import time
import datetime

DATE_FORMAT = "%Y-%m-%d"
DATE_TIME_FORMAT = DATE_FORMAT + " %H:%M:%S"

def utc_now():
    """returns current utc time"""
    now = datetime.datetime.utcnow()
    return now

def utc_now_epoch():
    """returns current utc time as epoch timestamp"""
    return int(time.time())

def  format_to_date_str(time_stamp):
    """Constructs and returns formatted date string, base on given timestamp"""
    return time_stamp.strftime(DATE_FORMAT)

def format_to_time_str(time_stamp):
    """Constructs and returns formatted time string, base on given timestamp"""
    return time_stamp.strftime(DATE_TIME_FORMAT)

def to_local_time(datetime_utc):
    """Converts utc time to local time"""
    return datetime_utc - datetime.timedelta(seconds=time.timezone)
