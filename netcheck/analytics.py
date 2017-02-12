"""This script is reponsible for reading/writing speed test result into local json/csv files."""

# Use DataDump class instance for this functionality
# fs structure : ./data
#                   /<date directory>
#                     /<date>.json         (global data file: contains all of the information)
#                     /<date>_uploads.csv  (pure csv file: only uploads mesurements)
#                     /<date>_downlads.csv (pure csv file: only downloads mesurements)
#                   /...

import json
import fsutil
import timeutil

def get_downloads_csv_data(time_stamp, config):
    """Reads csv content from downloads data file"""
    downloads_path = get_downloads_file_path(time_stamp, config)
    return fsutil.get_file_content(downloads_path)

def get_uploads_csv_data(time_stamp, config):
    """Reads csv content from upload data file"""
    uploads_path = get_uploads_file_path(time_stamp, config)
    return fsutil.get_file_content(uploads_path)


def get_downloads_file_path(time_stamp, config):
    """Constructs and returns downloads csv file absolute path"""
    time_str = timeutil.format_to_date_str(time_stamp)
    out_dir = get_output_dir(time_str, config)
    return out_dir + time_str +  config.DOWNLOADS_CSV_FILE_POSTFIX

def get_uploads_file_path(time_stamp, config):
    """Constructs and returns csv file absolute path"""
    time_str = timeutil.format_to_date_str(time_stamp)
    out_dir = get_output_dir(time_str, config)
    return out_dir + time_str +  config.UPLOADS_CSV_FILE_POSTFIX

def get_jsondata_file_path(time_stamp, config):
    """Constructs and returns json data file absolute path"""
    time_str = timeutil.format_to_date_str(time_stamp)
    out_dir = get_output_dir(time_str, config)
    return out_dir + time_str +  config.JSON_DATA_FILENAME

def get_output_dir(time_str, config):
    """Constructs and returns root directory of data files"""
    out_dir = config.ANALYTICS_OUTPUT_DIR + str(time_str) + "/"
    fsutil.recheck__dir(out_dir)
    return out_dir

class DataDump:
    """Responsible for writing data to local files as CSV/JSON"""
    def __init__(self, conf):
        self.__conf = conf

    def __dump_csv(self, value, file_path):
        fsutil.write_or_append(file_path, "," + str(value), str(value))


    def __dump_json(self, result, file_path):
        formatted = self.__format_to_json(result)
        json_data = fsutil.read_json_from_file(file_path)
        json_data.append(formatted)
        print(json_data)
        fsutil.write_to_file(file_path, json.dumps(json_data))

    def dump(self, result):
        """Writes speed test results to a files"""

        downloads_file = get_downloads_file_path(result.get_time_stamp, self.__conf)
        uploads_file = get_uploads_file_path(result.get_time_stamp, self.__conf)
        json_file = get_jsondata_file_path(result.get_time_stamp, self.__conf)

        self.__dump_csv(result.get_download_speed, downloads_file)
        self.__dump_csv(result.get_upload_speed, uploads_file)
        self.__dump_json(result, json_file)

    def __format_to_json(self, result):
        data = {}
        data["upload"] = str(result.get_upload_speed)
        data["download"] = str(result.get_download_speed)
        data["ping"] = str(result.get_ping_speed)
        time_str = timeutil.format_to_time_str(result.get_time_stamp)
        data["timeStamp"] = time_str
        json_str = json.dumps(data)
        return json_str
