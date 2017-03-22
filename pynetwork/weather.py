import json
import requests
import logging

TEL_AVIV_ID = 293397
LONDON_ID = 2643743

API_ID = "b1b15e88fa797225412429c1c50c122a1"
API_URL_FORMAT = "http://openweathermap.org/data/2.5/weather?id={0}&appid={1}"

def get_current_weather_data(city_code):
    """ Makes call to open weather map api
        Returns: weather data of given city code as json"""
    try:
        jsonResponse = requests.get(API_URL_FORMAT.format(city_code, API_ID))
        jsonObj = json.loads(jsonResponse.content)
        return jsonObj["main"]
    except Exception as e:
        logging.getLogger("PYNETWORK").exception(e)