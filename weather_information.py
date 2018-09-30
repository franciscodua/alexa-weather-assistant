import os
from botocore.vendored import requests
import json
import time
from datetime import datetime, timedelta

class DayWeatherInfo:
    def __init__(self, day_weather_info):
        utc_dt = datetime.utcfromtimestamp(day_weather_info['time'])
        # to account for daylight saving time in Portugal (UTC and UTC+1 during summer)
        # this way we always get the day right
        utc_plus_1 = utc_dt + timedelta(hours=1)
        self.date = utc_plus_1.date()
        self.precipitationProb = float(day_weather_info['precipProbability'])
        self.summary = day_weather_info['summary']
        self.minTemperature = day_weather_info['temperatureMin']
        self.maxTemperature = day_weather_info['temperatureMax']

class WeatherRepository:
    def request_information(self):
        raise NotImplementedError
    
    def get_by_date(self, date):
        response = self.request_information()
        day_info = next((info for info in response if info.date == date), None)
        if day_info is None:
            raise DayNotFoundException("Day " + str(date) + " not found! Weather information is only available for the next 7 days")
        return day_info
    
    def get_next_date(self, date):
        response = self.request_information()
        return next((info.date for info in response if info.date > date and not is_raining(info)[0]), None)


class APIWeatherRepository(WeatherRepository):
    def __init__(self):
        API_KEY = os.getenv("WEATHERAPIKEY", "")
        LATITUDE = os.getenv("WEATHERAPILATITUDE", "")
        LONGITUDE = os.getenv("WEATHERAPILONGITUDE", "")
        self.url = "https://api.darksky.net/forecast/{0}/{1},{2}?units=si&exclude=currently,minutely,alerts,hourly".format(API_KEY, LATITUDE, LONGITUDE)
        self.information = None

    def request_information(self):
        if self.information is None:
            response = requests.get(self.url)
            json_response = json.loads(response.content)
            print("API response: " + str(json_response))
            self.information = (DayWeatherInfo(day_info) for day_info in json_response['daily']['data'])
            print("Weather information: Call dark sky API: " + self.url)
        else:
            print("Weather information: Reused information from last call")        
        return self.information

class DayNotFoundException(Exception):
    pass

class WeatherAssistant:
    def __init__(self, rep = None):
        if rep is None:
            self.repository = APIWeatherRepository()
        else:
            self.repository = rep

    def rains_on_day(self, day):
        day_weather_info = self.repository.get_by_date(day)
        return is_raining(day_weather_info)
    
    def get_next_clear_day(self, day):
        return self.repository.get_next_date(day)

def is_raining(weatherInfo):
    return weatherInfo.precipitationProb > 0.2, weatherInfo.precipitationProb * 100
