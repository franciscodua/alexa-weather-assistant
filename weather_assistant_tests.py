import unittest
import json
import datetime as dt
from weather_information import WeatherAssistant, WeatherRepository
from weather_information import DayWeatherInfo, DayNotFoundException

# Added these tests so I don't have to use AWS lambda to validate every change

test_date = dt.date(2018, 7, 1)

class MockWeatherRepository(WeatherRepository):
    def request_information(self):
        with open("response_samples/dark_sky_sample.json") as f:
            data = json.load(f)
        return [DayWeatherInfo(day_info) for day_info in data['daily']['data']]

class WeatherInformationTests(unittest.TestCase):
    def test_successful_get_by_date_information(self):
        weatherassistant = WeatherAssistant(MockWeatherRepository())
        rains, prob = weatherassistant.rains_on_day(test_date)
        self.assertEqual(rains, True, "The expected answer was False: it won't rain")
        self.assertEqual(prob, 22, "We expeced a 22% probability of raining")
    
    def test_get_by_date_outside_seven_day_range(self):
        weatherassistant = WeatherAssistant(MockWeatherRepository())
        try:
            rain, prob = weatherassistant.rains_on_day(dt.datetime.today())
            self.fail("DayNotFoundException was expected. Instead function returned without error.\n" +\
            "With values for rain: " + str(rain) + "and for prob: " + str(prob))
        except DayNotFoundException:
            #this is the expected path
            pass

    def test_fail_get_next_date(self):
        weatherassistant = WeatherAssistant(MockWeatherRepository())
        date = weatherassistant.get_next_clear_day(test_date)
        self.assertIsNotNone(date)
        self.assertEqual(date, dt.date(2018, 7, 2))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
