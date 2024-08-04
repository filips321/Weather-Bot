from weather import *
from bottelegram import *
import asyncio

if __name__ == "__main__":

    weather = download_weather(read_geo_data())
    plot_charts(weather)

    asyncio.run(send_message_telegram(read_credentials(), 'bot test'))
