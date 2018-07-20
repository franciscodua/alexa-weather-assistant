import os
import datetime
from botocore.vendored import requests
import json

class DayWeatherInfo:
    def __init__(self, infoDict):
        self.date = get_date_from_response(infoDict)
        self.precipitationProb = long(infoDict['precipProbability'])
        self.summary = infoDict['summary']
        self.minTemperature = infoDict['temperatureMin']
        self.maxTemperature = infoDict['temperatureMax']

class WeatherInfo:
    def request_information(self):
        raise NotImplementedError
    
    def get(self):
        response = self.request_information()
        json_response = json.loads(response.content)
        daily_data = json_response['daily']['data']
        return dict(map(lambda x: (get_date_from_response(x), DayWeatherInfo(x)), daily_data))

class APIWeatherInfo(WeatherInfo):
    def __init__(self):
        API_KEY = os.getenv("WEATHERAPIKEY", "")
        LATITUDE = os.getenv("WEATHERAPILATITUDE", "")
        LONGITUDE = os.getenv("WEATHERAPILONGITUDE", "")
        self.url = "https://api.darksky.net/forecast/{0}/{1},{2}?units=si&exclude=currently,minutely,alerts,hourly".format(API_KEY, LATITUDE, LONGITUDE)

    def request_information(self):
        return requests.get(self.url)
    
# Used for tests
class JsonWeatherInfo(WeatherInfo):
    def request_information(self):
        with open('dark_sky_sample.json') as f:
            return json.load(f)

class DayNotFoundException(Exception):
    pass

def get_date_from_response(weather_day_data):
    return datetime.datetime.fromtimestamp(weather_day_data['time']).date()

def rains_on_day(day):
    daily_info_dict = APIWeatherInfo().get()
    if day not in daily_info_dict:
        raise DayNotFoundException("Day not found! Weather information is only available for the next 7 days")
    return is_raining(daily_info_dict[day])

def is_raining(weatherInfo):
    return weatherInfo.precipitationProb > 0.2, weatherInfo.precipitationProb * 100
