import json
import requests


def read_credentials():
    with open('../files/telegram-data.txt') as file:
        credentials = json.load(file)
    return credentials


def send_message_telegram(credentials, msg):
    api_token = credentials['api-token']
    group_id = credentials['group-id']

    telegram_api_url = f"https://api.telegram.org/bot{api_token}/sendMessage?chat_id=@{group_id}&text={msg}"
    telegram_response = requests.get(telegram_api_url)

    if telegram_response.status_code == 200:
        print('Notification has been sent on Telegram')
    else:
        print('Error with sending your message')
