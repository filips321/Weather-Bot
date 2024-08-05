import openmeteo_requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta, time
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
    hourly_df['date_hour'] = hourly_df['date'].dt.hour
    # hourly_df['date_hour'] = hourly_df['date'].dt.strftime('%H:%M')
    print(hourly_df)

    return hourly_df


def plot_charts(df):
    # Plotting
    plot_temperature_2m = df.plot(kind='line', x='date_hour', y='temperature_2m', color='#0A9036', legend=False,
                                       xlabel='', ylabel='')
    plt.title('Temperature - ' + date.today().strftime("%B %d, %Y"), fontweight='bold')
    plt.xlabel('Time [h]')
    plt.ylabel('Temperature [°C]')
    plt.ylim(df['temperature_2m'].min() - 5, df['temperature_2m'].max() + 5)
    plt.xticks(np.arange(df['date_hour'].min(), df['date_hour'].max() + 1, 1), rotation=45)
    plt.xlim(df['date_hour'].min(), df['date_hour'].max())
    plt.text(df['date_hour'].mean() - 1, df['temperature_2m'].max() + 4,
             'avg. ' + str(round(df['temperature_2m'].mean(), 1)) + ' °C', fontsize=11, style='italic')
    plt.figure(1).set_figwidth(10)

    plot_rain = df.plot(kind='bar', x='date_hour', y='rain', color='#0091FF', legend=False, xlabel='', ylabel='')
    plt.title('Rain - ' + date.today().strftime("%B %d, %Y"), fontweight='bold')
    plt.xlabel('Time [h]')
    plt.ylabel('Rain [mm]')
    plt.ylim(df['rain'].min(), df['rain'].max() + 5)
    plot_rain.set_xticklabels(np.arange(df['date_hour'].min(), df['date_hour'].max() + 1, 1))
    plt.xticks(rotation=45)
    plt.text(df['date_hour'].mean() - 7, df['rain'].max() + 4,
             'avg. ' + str(round(df['rain'].mean(), 1)) + ' mm', fontsize=11, style='italic')
    plt.figure(2).set_figwidth(10)

    plot_wind_speed_10m = df.plot(kind='line', x='date_hour', y='wind_speed_10m', color='#FF9A00', legend=False, xlabel='',
                                  ylabel='')
    plt.title('Wind - ' + date.today().strftime("%B %d, %Y"), fontweight='bold')
    plt.xlabel('Time [h]')
    plt.ylabel('Wind [m/s]')
    plt.ylim(0, df['wind_speed_10m'].max() + 5)
    plt.xticks(np.arange(df['date_hour'].min(), df['date_hour'].max() + 1, 1), rotation=45)
    plt.xlim(df['date_hour'].min(), df['date_hour'].max())
    plt.text(df['date_hour'].mean() - 1, df['wind_speed_10m'].max() + 4,
             'avg. ' + str(round(df['wind_speed_10m'].mean(), 1)) + ' m/s', fontsize=11, style='italic')
    plt.figure(3).set_figwidth(10)

    # plt.show()

    return plot_temperature_2m, plot_rain, plot_wind_speed_10m
