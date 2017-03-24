import json
import requests
import logging

API_ID = "b1b15e88fa797225412429c1c50c122a1"
API_URL_FORMAT = "http://openweathermap.org/data/2.5/weather?id={0}&appid={1}"

def get_current_weather_data(city_code):
    """ Makes call to open weather map api
        Returns: weather data of given city code as json"""
    try:
        json_response = requests.get(API_URL_FORMAT.format(city_code, API_ID))
        json_obj = json.loads(json_response.content)
        return json_obj["main"]
    except Exception as e:
        logging.getLogger("PYNETWORK").exception(e)
