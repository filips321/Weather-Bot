import openmeteo_requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import json


def read_geo_data():
    with open('../files/geo-data.txt') as file:
        geo_data = json.load(file)
    return geo_data


def download_weather(geo_data):
    om = openmeteo_requests.Client()
    params = {
        "latitude": geo_data["latitude"],
        "longitude": geo_data["longitude"],
        "timezone": "Europe/Warsaw",
        "forecast_days": 1,
        "hourly": ["temperature_2m", "rain", "wind_speed_10m"],
        "wind_speed_unit": "ms"
    }
    responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    response = responses[0]

    print()

    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")

    print()

    # Hourly values
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_rain = hourly.Variables(1).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(start=pd.to_datetime(hourly.Time(), unit="s") + pd.Timedelta(hours=2),
                                         # add 2 hours cuz GMT+2
                                         end=pd.to_datetime(hourly.TimeEnd(), unit="s") + pd.Timedelta(hours=2),
                                         # add 2 hours cuz GMT+2
                                         freq=pd.Timedelta(seconds=hourly.Interval()), inclusive="left"),
                   "temperature_2m": hourly_temperature_2m,
                   "rain": hourly_rain,
                   "wind_speed_10m": hourly_wind_speed_10m}

    hourly_df = pd.DataFrame(data=hourly_data).tail(18)
    print(hourly_df)

    return hourly_df


def plot_charts(df):
    # Plotting
    df.plot(kind='line', x='date', y='temperature_2m')
    plt.title('Temperature [°C] - ' + str(date.today().strftime('%B %d, %Y')))
    df.plot(kind='bar', x='date', y='rain')
    plt.title('Rain [mm] - ' + str(date.today().strftime('%B %d, %Y')))
    df.plot(kind='line', x='date', y='wind_speed_10m')
    plt.title('Wind [m/s] - ' + str(date.today().strftime('%B %d, %Y')))
    # plt.show()
