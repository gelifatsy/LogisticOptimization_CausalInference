import os
from datetime import datetime as dtime
import datetime
import requests

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

weather_api_key = os.getenv("WEATHERBIT_API_KEY")

class HistoricalWeatherFetcher():
    def __init__(self) -> None:
        self.URL = "https://api.weatherbit.io/v2.0/history/"
        self.API_KEY = weather_api_key
        self.visited_dates = {}

    def make_weather_api_request(self, lat, lng, start_date, end_date, time_range):
        api_url = f"{self.URL}daily?key={self.API_KEY}&lat={lat}&lon={lng}&start_date={start_date}&end_date={end_date}&units=I"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_weather_condition(self, data):
        precip = data['precip']
        clouds = data['clouds']

        if precip > 0:
            return 'Rainy'
        elif clouds > 50:
            return 'Cloudy'
        elif clouds < 20:
            return 'Sunny'
        else:
            return 'Partly Cloudy'

    def get_daily_weather(self, trip_origin, trip_start_time, time_of_day):
        lat, lng = trip_origin
        dt = dtime.strptime(trip_start_time, '%Y-%m-%d %H:%M:%S')
        start_date = f"{dt.year}-{dt.month}-{dt.day}"
        end_dt = dt + datetime.timedelta(days=1)
        end_date = f"{end_dt.year}-{end_dt.month}-{end_dt.day}"
        
        if start_date not in self.visited_dates or time_of_day not in self.visited_dates[start_date]:
            self.visited_dates.setdefault(start_date, {})[time_of_day] = "PERC"
            weather_data = self.make_weather_api_request(lat, lng, start_date, end_date, time_of_day)
            if weather_data:
                data = weather_data['data'][0]  # extract the first data point
                return self.get_weather_condition(data)
            else:
                return None
        else:
            return self.visited_dates[start_date][time_of_day]

if __name__ == "__main__":
    w = HistoricalWeatherFetcher()
    trip_origin = (6.508813001668548, 3.37740316890347)
    trip_start_time = "2021-07-01 07:28:04"
    time_of_day = "morning"
    weather_data = w.get_daily_weather(trip_origin, trip_start_time, time_of_day)
    print(weather_data)