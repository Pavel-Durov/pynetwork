#!/usr/bin/python
""" Network Upload, Download, Ping speed check script"""

import json
import slack
import timeutil
import chart
import weather
import argparse
import fsutil
import timeutil
import pyspeedtest
import logging
import convertutil
from mail import EmailSender
from mail import MessageFormatter
from models import GlobalConfig
from models import SpeedTestResult
from gdrive import GoogleDriveApi


__program__ = 'PYNETWORK'
__version__ = '1.0.0'
__description__ = 'Network ping/upload/download speed measurements analysis and reports'

GlobalConfig.init_logger()
LOG = logging.getLogger(__program__)

def __check_speed():
    LOG.info("Network speed check is running")
    time_stamp = timeutil.utc_now()

    speed_test = pyspeedtest.SpeedTest()

    download = convertutil.bytes_to_mb(speed_test.download())
    LOG.info("download speed: " + str(download))
    upload = convertutil.bytes_to_mb(speed_test.upload())
    LOG.info("upload speed: " + str(upload))
    ping = round(speed_test.ping(), 2)
    LOG.info("ping speed: " + str(ping))

    return SpeedTestResult(download, upload, ping, time_stamp)

def main(config=None):
    """Main entry point"""
    LOG = logging.getLogger(__program__)

    if config.get_real_network_check:
        speed_result = __check_speed()
    else:
        speed_result = SpeedTestResult(2, 3, 4, timeutil.utc_now())

    if config.get_weather_samples_configured:
        weather_data = weather.get_current_weather_data(config.get_openweather_api_city_code)
        speed_result.set_weather_data(weather_data)

    data_file_path = fsutil.get_jsondata_file_path(speed_result.get_time_stamp, config)
    fsutil.write_speed_result_json(speed_result, data_file_path)

    emf = MessageFormatter(config)
    message = emf.format_message(speed_result)

    utc_time_stamp = speed_result.get_time_stamp

    charGenerator = chart.ChartGenerator(config)
    chart_path = charGenerator.generate_chart(utc_time_stamp)
    chart_image_path = charGenerator.generate_chart_image(utc_time_stamp)

    local_time = timeutil.to_local_time(utc_time_stamp)
    __send_hourly_mail(config, local_time, message, chart_image_path)

    __update_slack(config, speed_result)

    google_drive = GoogleDriveApi()
    __gdrive_data_upload(google_drive, config, local_time, data_file_path)
    __gdrive_chart_upload(google_drive, config, local_time, chart_path)

    LOG.info("pynetwork, main routine end")

def __update_slack(config, speed_result):
    slack_config = config.get_slack_config
    if slack_config and slack_config.get_enabled:
        bot = slack.SlackPyNetworkBot(config)
        message = bot.compose_speed_result_message(speed_result)
        bot.send_message(message, slack_config.get_channel)

def __send_hourly_mail(config, local_time, message, chart_image_path):
    email_sender = EmailSender(config)
    if config.get_send_hourly_mail(local_time):
        email_sender.send_gmail(message, chart_image_path)

def __gdrive_data_upload(gdrive, config, local_time, data_file_path):
    if config.get_upload_daily_data_gdrive(local_time):
        file_name = fsutil.get_file_name(data_file_path)
        gdrive.upload_json_file(file_name, data_file_path)

def __gdrive_chart_upload(gdrive, config, local_time, data_file_path):
    upload = config.get_upload_daily_chart_gdrive(local_time)
    if upload and fsutil.file_exist(data_file_path):
        file_name = fsutil.get_file_name(data_file_path)
        gdrive.upload_html_file(file_name, data_file_path)

def _parse_args():
    arg_parser = argparse.ArgumentParser(
        description=__description__,
        usage='%(prog)s [OPTION]...')

    arg_parser.add_argument("-d", help="Download speed constraint", type=float)
    arg_parser.add_argument("-u", help="Upload speed constraint", type=float)
    arg_parser.add_argument("-p", help="Ping speed constraint", type=float)

    args = arg_parser.parse_args()
    return GlobalConfig(args.u, args.d, args.p)

if __name__ == "__main__":
    main(_parse_args())
