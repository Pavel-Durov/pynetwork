"""Utility script for filesystem management"""

import os
import json
import logging
from json import JSONEncoder

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
