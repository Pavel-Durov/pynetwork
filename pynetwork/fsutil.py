"""Utility script for filesystem management"""

import os
import json
import logging
import timeutil
from json import JSONEncoder

def get_jsondata_file_path(time_stamp, config):
    """Constructs and returns json data file absolute path"""
    time_str = timeutil.format_to_date_str(time_stamp)
    out_dir = get_output_dir(time_str, config)
    return out_dir + time_str +  config.JSON_DATA_FILENAME

def get_output_dir(time_str, config):
    """Constructs and returns root directory of data files"""
    out_dir = config.ANALYTICS_OUTPUT_DIR + str(time_str) + "/"
    recheck__dir(out_dir)
    return out_dir

def __append_json(json_content, file_path):
    json_data = read_json_from_file(file_path)
    json_data.append(json_content)

    write_json_to_file(file_path, json_data)

def write_speed_result_json(speet_result, path, weather_data):
    """
        Writes speed test results to a json file
    """
    formatted = __format_to_json(speet_result, weather_data)
    __append_json(formatted, path)

def __format_to_json(result, weather_data):
    data = {}
    data["upload"] = str(result.get_upload_speed)
    data["download"] = str(result.get_download_speed)
    data["ping"] = str(result.get_ping_speed)
    # time_str = timeutil.format_to_time_str(result.get_time_stamp)
    data["utcEpoch"] = timeutil.utc_now_epoch()
    data["weather"] = weather_data
    return data


def recheck__dir(daily_dir):
    """Creates directory if not exists"""
    if os.path.exists(daily_dir) is False:
        os.makedirs(daily_dir)

def file_exist(path):
    """Returns whether the file exists"""
    return os.path.exists(path)

def write_or_append(file_path, append_value, write_value):
    """Appends or write to files, depends on whether the file exist or not:
        appends of file exists, writes otherwise"""
    try:
        if file_exist(file_path):
            out_file = open(file_path, "a")
            out_file.write(append_value)
        else:
            out_file = open(file_path, "w")
            out_file.write(write_value)

        out_file.close()
    except IOError as e:
        logging.getLogger("PYNETWORK").exception(e)

def write_to_file(path, content):
    """Writes content to specified absolute file path"""
    try:
        with open(path, 'w') as file:
            file.write(content)
    except IOError as e:
        logging.getLogger("PYNETWORK").exception(e)

def write_json_to_file(path, data):
    """Writes json object to specified absolute file path"""
    try:
        with open(path, 'w') as outfile:
            json.dump(data, outfile)
    except IOError as e:
        logging.getLogger("PYNETWORK").exception(e)


def get_file_content(file_path):
    """Reads and returns content of a file"""
    try:
        with open(file_path, 'r') as content_file:
            return content_file.read()
    except IOError as e:
        logging.getLogger("PYNETWORK").exception(e)

def read_json_from_file(file_path):
    """Reads or creates new file if not exists"""
    try:
        if file_exist(file_path):
            with open(file_path) as json_file:
                raw_json = json_file.read()
            return json.loads(raw_json)
        else:
            with open(file_path, 'w') as json_file:
                json_file.write("")

            return json.loads("[]")
    except IOError as e:
        logging.getLogger("PYNETWORK").exception(e)

def get_file_name(filename):
    """Returns file name from path"""
    splitted = filename.split("/")
    return filename.split("/")[len(splitted) -1]
