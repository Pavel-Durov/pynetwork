"""This script is reponsible for reading/writing speed test result into local json/csv files."""

# Use DataDump class instance for this functionality
# fs structure : ./data
#                   /<date directory>
#                     /<date>.json         (global data file: contains all of the information)


import json
import fsutil
import timeutil

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

    def __dump_json(self, result, file_path):
        formatted = self.__format_to_json(result)
        json_data = fsutil.read_json_from_file(file_path)
        json_data.append(formatted)

        fsutil.write_json_to_file(file_path, json_data)

    def dump(self, result):
        """Writes speed test results to a files"""
        json_file = get_jsondata_file_path(result.get_time_stamp, self.__conf)
        self.__dump_json(result, json_file)

    def __format_to_json(self, result):
        data = {}
        data["upload"] = str(result.get_upload_speed)
        data["download"] = str(result.get_download_speed)
        data["ping"] = str(result.get_ping_speed)
        time_str = timeutil.format_to_time_str(result.get_time_stamp)
        data["timeStamp"] = time_str

        return data
