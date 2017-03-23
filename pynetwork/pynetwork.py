#!/usr/bin/python
""" Network Upload, Download, Ping speed check script"""

import json
import timeutil
import chart
import weather
import argparse
import fsutil
import timeutil
import pyspeedtest
import logging
from mail import EmailSender
from mail import MessageFormatter
from models import GlobalConfig
from models import SpeedTestResult
from gdrive import GoogleDriveApi

def __check_speed():
    log = logging.getLogger("PYNETWORK")
    log.info("Network speed check is running")

    time_stamp = timeutil.utc_now()

    speed_test = pyspeedtest.SpeedTest()
    download = round(speed_test.download() / 1000 / 1000, 2)
    log.info("download speed: " + str(download))
    upload = round(speed_test.upload() / 1000 / 1000, 2)
    log.info("upload speed: " + str(upload))
    ping = round(speed_test.ping(), 2)
    log.info("ping speed: " + str(ping))

    return SpeedTestResult(download, upload, ping, time_stamp)

def main(config):
    """Main function"""
    log = logging.getLogger("PYNETWORK")

    if config.get_real_network_check:
        speed_result = __check_speed()
    else:
        speed_result = SpeedTestResult(2, 3, 4, timeutil.utc_now())
    
    weather_data = weather.get_current_weather_data(weather.TEL_AVIV_ID)

    data_file_path = fsutil.get_jsondata_file_path(speed_result.get_time_stamp, config)
    fsutil.write_speed_result_json(speed_result, data_file_path, weather_data)

    emf = MessageFormatter(config)
    message = emf.format_message(speed_result)

    utc_time_stamp = speed_result.get_time_stamp
    chart.ChartGenerator(config).generate_chart(utc_time_stamp)
    chart_path = chart.ChartGenerator(config).generate_chart(utc_time_stamp)

    local_time = timeutil.to_local_time(utc_time_stamp)
    __send_hourly_mail(config, local_time, message)

    google_drive = GoogleDriveApi()

    __upload_daily_data_gdrive(google_drive,
                               config,
                               local_time,
                               data_file_path)

    __upload_daily_chart_to_gdrive(google_drive,
                                   config,
                                   local_time,
                                   chart_path)


    log.info("pynetwork, main routine end")

def __send_hourly_mail(config, local_time, message):
    email_sender = EmailSender(config)
    if config.get_send_hourly_mail(local_time):
        email_sender.send_gmail(message)

def __upload_daily_data_gdrive(gdrive, config, local_time, data_file_path):
    if config.get_upload_daily_data_gdrive(local_time):
        file_name = fsutil.get_file_name(data_file_path)
        gdrive.upload_json_file(file_name, data_file_path)

def __upload_daily_chart_to_gdrive(gdrive, config, local_time, data_file_path):
    upload = config.get_upload_daily_chart_gdrive(local_time)
    if upload and fsutil.file_exist(data_file_path):
        file_name = fsutil.get_file_name(data_file_path)
        gdrive.upload_html_file(file_name, data_file_path)


def _parse_args():
    arg_parser = argparse.ArgumentParser(
        description='Network upload, download, ping speed check and notifications script',
        usage='%(prog)s [OPTION]...')

    arg_parser.add_argument("-d", help="Download speed constraint", type=float)
    arg_parser.add_argument("-u", help="Upload speed constraint", type=float)
    arg_parser.add_argument("-p", help="Ping speed constraint", type=float)

    args = arg_parser.parse_args()
    return GlobalConfig(args.u, args.d, args.p)

if __name__ == "__main__":
    GlobalConfig.init_logger()
    main(_parse_args())
