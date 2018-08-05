import os
from botocore.vendored import requests
import json
import time

class DayWeatherInfo:
    def __init__(self, day_weather_info):
        self.date = int(day_weather_info['time'])
        self.precipitationProb = long(day_weather_info['precipProbability'])
        self.summary = day_weather_info['summary']
        self.minTemperature = day_weather_info['temperatureMin']
        self.maxTemperature = day_weather_info['temperatureMax']

class WeatherInfo:
    def request_information(self):
        raise NotImplementedError
    
    def get_by_date(self, date):
        response = self.request_information()
        json_response = json.loads(response.content)
        daily_data = json_response['daily']['data']
        # convert date to timestamp
        timestamp = time.mktime(date.timetuple())
        day_info = next((info for info in daily_data if info['time'] == timestamp), None)
        if day_info is None:
            raise DayNotFoundException("Day not found! Weather information is only available for the next 7 days")
        return DayWeatherInfo(day_info)

class APIWeatherInfo(WeatherInfo):
    def __init__(self):
        API_KEY = os.getenv("WEATHERAPIKEY", "")
        LATITUDE = os.getenv("WEATHERAPILATITUDE", "")
        LONGITUDE = os.getenv("WEATHERAPILONGITUDE", "")
        self.url = "https://api.darksky.net/forecast/{0}/{1},{2}?units=si&exclude=currently,minutely,alerts,hourly".format(API_KEY, LATITUDE, LONGITUDE)
        self.information = None

    def request_information(self):
        if self.information is None:
            self.information = requests.get(self.url)
            print("Weather information: Call dark sky API: " * self.url)
        else:
            print("Weather information: Reused information from last call")
        return self.information
    
# Used for tests
class JsonWeatherInfo(WeatherInfo):
    def request_information(self):
        with open('dark_sky_sample.json') as f:
            return json.load(f)

class DayNotFoundException(Exception):
    pass

weather_info = APIWeatherInfo()

def rains_on_day(day):
    day_weather_info = weather_info.get_by_date(day)
    return is_raining(day_weather_info)

def is_raining(weatherInfo):
    return weatherInfo.precipitationProb > 0.2, weatherInfo.precipitationProb * 100
