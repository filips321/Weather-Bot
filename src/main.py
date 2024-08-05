from weather import *
from bottelegram import *
import asyncio
from datetime import date

# import emoji

if __name__ == "__main__":
    weather = download_weather(read_geo_data())
    plots = plot_charts(weather)

    asyncio.run(send_message_telegram(read_credentials(),
                                      'Wake up BRO, it\'s 6am already! \U0001f976\n\nYour daily weather report for:\n' + str(
                                          date.today().strftime('%d/%m/%Y'))))
    asyncio.run(send_message_telegram(read_credentials(), plots[0]))
    asyncio.run(send_message_telegram(read_credentials(), plots[1]))
    asyncio.run(send_message_telegram(read_credentials(), plots[2]))
    asyncio.run(send_message_telegram(read_credentials(), '========== \U0001F9FF =========='))
