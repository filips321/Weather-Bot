import json
import telegram
import matplotlib
from io import BytesIO


def read_credentials():
    with open('../files/telegram-data.txt') as file:
        credentials = json.load(file)
    return credentials


async def send_message_telegram(credentials, msg):
    api_token = credentials['api-token']
    group_id = '@' + credentials['group-id']

    bot = telegram.Bot(api_token)
    if isinstance(msg, str):
        await bot.sendMessage(group_id, msg)
    elif type(msg) == matplotlib.axes._axes.Axes:
        msg_plot = prepare_plot(msg)
        await bot.sendPhoto(group_id, msg_plot)
    else:
        print('ERROR: Wrong type of message')


def prepare_plot(plot):  # Write the plot Figure to a file-like bytes object
    plot_file = BytesIO()
    fig = plot.get_figure()
    fig.savefig(plot_file, format='png')
    plot_file.seek(0)

    prepared_plot = plot_file

    return prepared_plot
