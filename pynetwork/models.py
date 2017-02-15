import os
import fsutil
import datetime

class GlobalConfig:
    """Global configuration for network speed check"""

    PROJ_PATH = ''
    MAIN_CSS_PATH = ''
    OUTPUT_HTML_FILE = ''
    ANALYTICS_OUTPUT_DIR = ''
    CHART_HTML_DIR = ''
    CONFIG_JSON_FILE = ''
    CHART_HTML_POSTFIX = "_chart.html"
    DOWNLOADS_CSV_FILE_POSTFIX = "_downloads.csv"
    UPLOADS_CSV_FILE_POSTFIX = "_uploads.csv"
    JSON_DATA_FILENAME = "_data.json"

    UNSET_CONSTRAINT = -1


    def __init__(self, upload_constraint, download_constraint, ping_constraint):

        self.__upload_constraint = self.__check_for_none(upload_constraint)
        self.__download_constraint = self.__check_for_none(download_constraint)
        self.__ping_constraint = self.__check_for_none(ping_constraint)

        #Paths set
        self.PROJ_PATH = os.path.dirname(os.path.abspath(__file__))
        self.MAIN_CSS_PATH = self.PROJ_PATH + "/css/mail.css"
        self.OUTPUT_HTML_FILE = self.PROJ_PATH + "/html/email.html"
        self.ANALYTICS_OUTPUT_DIR = self.PROJ_PATH + "/data/"
        self.CHART_HTML_DIR = self.PROJ_PATH + "/html/"
        self.CONFIG_JSON_FILE = self.PROJ_PATH + "/../config.json"

        json_config = fsutil.read_json_from_file(self.CONFIG_JSON_FILE)

        #Sets whether use real time network check (mainly used for DEBUG purposes)
        self.__real_network_check = json_config["realNetworkCheck"]
        #Sets whether writing local file with the mail html content
        self.__write_to_local_html_file = json_config["writeLocalHtml"]
        #Sets whether send a mail when network check is completed"""
        self.__send_mail = json_config["sendMail"]
        #Sets for attaching chart html to mail
        self.__attach_mail_chart = json_config["attachMailChart"]

        self.__receiver_gmail_account = json_config["receiverGmailAccount"]
        self.__agent_gmail_account = json_config["agentGmailAccount"]
        #This is way insecure : Figureout how to sore password in more reliable way (keyring?)
        self.__agent_gmail_password = json_config["agentGmailPassword"]

        self.__upload_results_to_gdrive = json_config["uploadResultsToGdrive"]


    @property
    def get_upload_results_to_gdrive(self):
        """Configuration for whether upload test reusult to google drive"""
        return self.__upload_results_to_gdrive

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
        return time_stamp.hour in [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]


class SpeedTestResult:
    """Contains speed test result"""

    def __init__(self, download, upload, ping, utc_time):
        self.__download = download
        self.__upload = upload
        self.__ping = ping
        self.__measurement_utc_time = utc_time

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
