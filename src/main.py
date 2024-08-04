from weather import *
from telegram import *

if __name__ == "__main__":

    weather = download_weather(read_geo_data())
    plot_charts(weather)

    send_message_telegram(read_credentials(), 'hej')
