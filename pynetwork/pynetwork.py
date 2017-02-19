#!/usr/bin/python
""" Network Upload, Download, Ping speed check script"""

import chart
import argparse
import fsutil
import timeutil
import pyspeedtest
from mail import EmailSender
from mail import MessageFormatter
from models import GlobalConfig
from models import SpeedTestResult
from analytics import DataDump
from gdrive import GoogleDriveApi

def __check_speed():
    print("Network speed check is running")

    speed_test = pyspeedtest.SpeedTest()
    download = round(speed_test.download() / 1000 / 1000, 2)
    print("download speed: " + str(download))
    upload = round(speed_test.upload() / 1000 / 1000, 2)
    print("upload speed: " + str(upload))
    ping = round(speed_test.ping(), 2)
    print("ping speed: " + str(ping))

    return SpeedTestResult(download, upload, ping, timeutil.utc_now())

def __main(config):
    if config.get_real_network_check:
        speed_result = __check_speed()
    else:
        speed_result = SpeedTestResult(2, 3, 4, timeutil.utc_now())

    log = DataDump(config)
    log.dump(speed_result)

    emf = MessageFormatter(config)
    message = emf.format_message(speed_result)

    email_sender = EmailSender(config)
    time_stamp = speed_result.get_time_stamp

    chart.ChartGenerator(config).generate_chart(time_stamp)

    if config.get_send_mail and config.is_legit_hour_for_mail(time_stamp):
        email_sender.send_gmail(message)

    chart_path = chart.ChartGenerator(config).generate_chart(time_stamp)

    if config.get_upload_results_to_gdrive and fsutil.file_exist(chart_path):
        file_name = fsutil.get_file_name(chart_path)
        GoogleDriveApi().upload_html_file(file_name, chart_path)

def main():

    arg_parser = argparse.ArgumentParser(
        description='Network upload, download, ping speed check and notifications script',
        usage='%(prog)s [OPTION]...')

    arg_parser.add_argument("-d", help="Download speed constraint", type=float)
    arg_parser.add_argument("-u", help="Upload speed constraint", type=float)
    arg_parser.add_argument("-p", help="Ping speed constraint", type=float)

    args = arg_parser.parse_args()

    configuration = GlobalConfig(args.u, args.d, args.p)

    __main(configuration)

if __name__ == "__main__":
    main()




