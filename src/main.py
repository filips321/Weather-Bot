from weather import *
from bottelegram import *
import asyncio

if __name__ == "__main__":

    weather = download_weather(read_geo_data())
    plots = plot_charts(weather)
    s = 'czesc'
    print(type(s))
    asyncio.run(send_message_telegram(read_credentials(), 'bot test'))
    asyncio.run(send_message_telegram(read_credentials(), plots[0]))
    asyncio.run(send_message_telegram(read_credentials(), 1))
    # asyncio.run(send_message_telegram(read_credentials(), 'bot test'))
