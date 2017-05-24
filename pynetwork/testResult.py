import timeutil

class TestResult(object):
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
    def get_default(self):
        """Returns default test result instance"""
        return TestResult(2, 3, 4, timeutil.utc_now())

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

