import os
import json
import requests
import logging

WEATHER_APP_ID_ENV_KEY = "WEATHER_APP_ID"
API_URL_FORMAT = "http://openweathermap.org/data/2.5/weather?id={0}&appid={1}"

def get_current_weather_data(city_code):
    """ Makes call to open weather map api
        Returns: weather data of given city code as json"""
    try:
        app_id = __wather_app_id()
        if app_id:
            json_response = requests.get(API_URL_FORMAT.format(city_code, app_id))
            json_obj = json.loads(json_response.content)
            return json_obj["main"]
    except Exception as e:
        logging.getLogger("PYNETWORK").exception(e)

@property
def __wather_app_id():
    if WEATHER_APP_ID_ENV_KEY in os.environ:
        return os.environ[WEATHER_APP_ID_ENV_KEY]
