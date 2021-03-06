"""Utility script for filesystem management"""

import os
import json
import logging
import timeutil

def swap_path_extention(chart_path, extention):
    """
        Returns:
            same filename with diffrent extention
    """
    file_name, ext = os.path.splitext(chart_path)
    return file_name + extention

def get_jsondata_file_path(time_stamp, config):
    """Constructs and returns json data file absolute path"""
    time_str = timeutil.format_to_date_str(time_stamp)
    out_dir = get_data_output_dir(time_str, config)
    return out_dir + time_str +  config.JSON_DATA_FILENAME

def get_data_output_dir(time_str, config):
    """Constructs and returns root directory of data files"""
    out_dir = config.DATA_OUTPUT_DIR + str(time_str) + "/"
    recheck_dir(out_dir)
    return out_dir

def write_speed_result_json(speet_result, path):
    """
        Writes speed test results to a json file
    """
    json_data = read_json_from_file(path)
    json_data.append(speet_result.to_json())
    write_json_to_file(path, json_data)

def recheck_dir(dir):
    """Creates directory if not exists"""
    if os.path.exists(dir) is False:
        os.makedirs(dir)

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
