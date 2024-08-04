import json
import requests
import telegram


def read_credentials():
    with open('../files/telegram-data.txt') as file:
        credentials = json.load(file)
    return credentials


async def send_message_telegram(credentials, msg):
    api_token = credentials['api-token']
    group_id = '@' + credentials['group-id']

    bot = telegram.Bot(api_token)
    await bot.send_message(group_id, msg)
