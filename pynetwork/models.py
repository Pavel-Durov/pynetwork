import os
import fsutil
import datetime
import timeutil
import logging
import logging.handlers


LEGIT_EMAIL_HOURS = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
LOG_NAME = "PYNETWORK"

class GlobalConfig(object):
    """Global configuration for network speed check"""

    PROJ_PATH = None
    MAIN_CSS_PATH = None
    OUTPUT_HTML_FILE = None
    DATA_OUTPUT_DIR = None
    CHART_HTML_DIR = None
    CONFIG_JSON_FILE = None
    CHART_HTML_POSTFIX = "_chart.html"
    DOWNLOADS_CSV_FILE_POSTFIX = "_downloads.csv"
    UPLOADS_CSV_FILE_POSTFIX = "_uploads.csv"
    JSON_DATA_FILENAME = "_data.json"
    JSON_WEATHER_DATA_FILENAME = "_weather_data.json"
    SCRIPT_LAST_RUNNING_HOUR = 0
    UNSET_CONSTRAINT = -1
    PYNETWORK_GMAIL_CREDENTIALS_ENV_KEY = "PYNETWORK_GMAIL_CREDENTIALS"

    def __init__(self, upload_constraint, download_constraint, ping_constraint):

        self.__upload_constraint = self.__check_for_none(upload_constraint)
        self.__download_constraint = self.__check_for_none(download_constraint)
        self.__ping_constraint = self.__check_for_none(ping_constraint)

        #Paths set
        self.PROJ_PATH = os.path.dirname(os.path.abspath(__file__))
        self.MAIN_CSS_PATH = self.PROJ_PATH + "/css/mail.css"
        self.OUTPUT_HTML_FILE = self.PROJ_PATH + "/html/email.html"
        self.DATA_OUTPUT_DIR = self.PROJ_PATH + "/data/"
        self.CHART_HTML_DIR = self.PROJ_PATH + "/html/"
        self.CONFIG_JSON_FILE = self.PROJ_PATH + "/../config.json"
        self.SECRETS_JSON_FILE = self.PROJ_PATH + "/secrets/mail.secret.json"

        json_config = fsutil.read_json_from_file(self.CONFIG_JSON_FILE)

        #Sets whether use real time network check (mainly used for DEBUG purposes)
        self.__real_network_check = json_config["realNetworkCheck"]
        #Sets whether writing local file with the mail html content
        self.__write_to_local_html_file = json_config["writeLocalHtml"]

        self.__slack_bot_enabled = json_config["slackBotEnabled"]

        mail_config = json_config["mail"]
        if mail_config:
            #Sets whether send a mail when network check is completed"""
            self.__send_mail = mail_config["sendMail"]
            #Sets for attaching chart html to mail
            self.__attach_mail_chart = mail_config["attachMailChart"]

        gdrive_config = json_config["gdrive"]
        if gdrive_config:
            self.__upload_daily_chart_to_gdrive = gdrive_config["uploadDailyChart"]
            self.__upload_daily_data_to_gdrive = gdrive_config["uploadDailyData"]

        weather_config = json_config["weather"]
        if weather_config:
            self.__take_weather_samples = weather_config["takeWeatherSamples"]
            self.__open_weather_api_city_code = weather_config["openWeatherAPICityCode"]

        self.__fetch_gmail_credentials()

    def __fetch_gmail_credentials(self):
        if self.PYNETWORK_GMAIL_CREDENTIALS_ENV_KEY in os.environ:
            try:
                secret = os.environ["PYNETWORK_GMAIL_CREDENTIALS"]
                splitted = secret.split(";")
                self.__receiver_gmail_account = splitted[0]
                self.__agent_gmail_account = splitted[1]
                self.__agent_gmail_password = splitted[2]
            except Exception as ex:
                logging.getLogger("PYNETWORK").exception(ex)
        else:
            self.__send_mail = False

    @staticmethod
    def init_logger():
        """Initialize logger"""
        my_logger = logging.getLogger(LOG_NAME)
        my_logger.setLevel(logging.DEBUG)
        fsutil.recheck__dir("logs")
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler("logs/pynetwork.out",
                                                       maxBytes=2000)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        my_logger.addHandler(handler)

    def get_upload_daily_data_gdrive(self, local_time):
        """
            Checks the given time for last hour of a day , and config settings.
            Returns: whether to upload the data file to google drive
        """
        last_hour_of_day = local_time.hour == self.SCRIPT_LAST_RUNNING_HOUR
        return self.__upload_daily_data_to_gdrive and last_hour_of_day

    def get_upload_daily_chart_gdrive(self, local_time):
        """
            Checks the given time for last hour of a day , and config settings.
            Returns: whether to upload the resut chart to google drive
        """
        last_hour_of_day = local_time.hour == self.SCRIPT_LAST_RUNNING_HOUR
        return self.__upload_daily_chart_to_gdrive and last_hour_of_day

    def get_send_hourly_mail(self, local_time):
        """
            Checks the given time for legit hour and configuration setting,
                            mail sent only on round hours - e.g every hour.
            Returns: whether to send mail
        """
        legit = self.is_legit_hour_for_mail(local_time)
        return self.get_send_mail and legit and local_time.minute == 0

    @property
    def get_slack_bot_enabled(self):
        """Returns whether slack bot is configured"""
        return self.__slack_bot_enabled

    @property
    def get_openweather_api_city_code(self):
        """Returns: city code by open weather api convention
           Exaples: TEL_AVIV_ID = 293397, LONDON_ID = 2643743
        """
        return self.__open_weather_api_city_code

    @property
    def get_weather_samples_configured(self):
        "Returns: whether to include weather data"
        return self.__take_weather_samples

    @property
    def get_receiver_gmail_account(self):
        """Receiver gmail account"""
        return self.__receiver_gmail_account

    @property
    def get_agent_gmail_account(self):
        """Agent gmail account"""
        return self.__agent_gmail_account

    @property
    def get_agent_gmail_password(self):
        """Agent gmail password"""
        return self.__agent_gmail_password

    @property
    def get_write_html_file(self):
        """Configuration for writing local file with the mail html content"""
        return self.__write_to_local_html_file

    @property
    def get_upload_constraint(self):
        """Configuration for speed check upload limit"""
        return self.__upload_constraint

    @property
    def get_downlad_constraint(self):
        """Configuration for speed check download limit"""
        return self.__download_constraint

    @property
    def get_ping_constraint(self):
        """Configuration for speed check ping limit"""
        return self.__ping_constraint

    @property
    def get_real_network_check(self):
        """Configuration whether use real time network check (mainly used for DEBUG purposes)"""
        return self.__real_network_check

    @property
    def get_send_mail(self):
        """Configuration for whether send a mail when network check is completed"""
        return self.__send_mail

    @property
    def get_attach_mail_chart(self):
        """Configuration for attaching chart html to mail"""
        return self.__attach_mail_chart

    def __check_for_none(self, value):
        if value is None:
            return self.UNSET_CONSTRAINT
        else:
            return value

    @staticmethod
    def is_legit_hour_for_mail(time_stamp):
        """Checks whether the given date is in range of email sending hours configuration"""
        return time_stamp.hour in LEGIT_EMAIL_HOURS


class SpeedTestResult(object):
    """Contains speed test result"""

    def __init__(self, download, upload, ping, utc_time):
        self.__download = download
        self.__upload = upload
        self.__ping = ping
        self.__measurement_utc_time = utc_time
        self.__weather_data = None

    def set_weather_data(self, weather_data):
        """Returns utc time of the measurement"""
        self.__weather_data = weather_data

    @property
    def get_weather_data(self):
        """Returns weather data at the measurement time"""
        return self.__weather_data

    @property
    def get_time_stamp(self):
        """Returns utc time of the measurement"""
        return self.__measurement_utc_time

    @property
    def get_download_speed(self):
        """Returns download speed of network speed test"""
        return self.__download

    @property
    def get_upload_speed(self):
        """Returns upload speed of network speed test"""
        return self.__upload

    @property
    def get_ping_speed(self):
        """Returns ping speed of network speed test"""
        return self.__ping

    def to_json(self):
        """
            Returns: json object, representing SpeedTestResult data
        """
        data = {}
        data["upload"] = str(self.get_upload_speed)
        data["download"] = str(self.get_download_speed)
        data["ping"] = str(self.get_ping_speed)
        data["utcEpoch"] = timeutil.utc_now_epoch()
        if self.get_weather_data:
            data["weather"] = self.get_weather_data
        return data
