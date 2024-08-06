from weather import *
from bottelegram import *
import asyncio
from datetime import date


# Option 1 - AWS
def lambda_handler(event, context):
    df_weather = download_weather(read_geo_data())
    plots = plot_charts(df_weather)

    asyncio.run(send_message_telegram(read_credentials(),
                                      'Wake up BRO, it\'s 6am already! \U0001f976\n\nYour daily weather report for:\n' + str(
                                          round(read_geo_data()['latitude'], 2)) + ', ' + str(
                                          round(read_geo_data()['longitude'], 2)) + '\n' + str(
                                          date.today().strftime('%d/%m/%Y'))))
    asyncio.run(send_message_telegram(read_credentials(), plots[0]))
    asyncio.run(send_message_telegram(read_credentials(), plots[1]))
    asyncio.run(send_message_telegram(read_credentials(), plots[2]))
    asyncio.run(send_message_telegram(read_credentials(), '========== \U0001F9FF =========='))
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda implemented properly!')
    }


# Option 2 - local
# if __name__ == "__main__":
#     df_weather = download_weather(read_geo_data())
#     plots = plot_charts(df_weather)
#
#     asyncio.run(send_message_telegram(read_credentials(),
#                                       'Wake up BRO, it\'s 6am already! \U0001f976\n\nYour daily weather report for:\n' + str(
#                                           round(read_geo_data()['latitude'], 2)) + ', ' + str(
#                                           round(read_geo_data()['longitude'], 2)) + '\n' + str(
#                                           date.today().strftime('%d/%m/%Y'))))
#     asyncio.run(send_message_telegram(read_credentials(), plots[0]))
#     asyncio.run(send_message_telegram(read_credentials(), plots[1]))
#     asyncio.run(send_message_telegram(read_credentials(), plots[2]))
#     asyncio.run(send_message_telegram(read_credentials(), '========== \U0001F9FF =========='))
