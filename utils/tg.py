from telethon.sync import TelegramClient, events
from conf import config


def send_msg_to_tg(msg):
    """
    :param msg:
    :return:
    """
    with TelegramClient(config.JY_TG_SESSION_PATH, config.JY_TG_API_ID, config.JY_TG_API_HASH) as client:
        item_list = config.JY_TG_RECEIVER_LINK.split(',')
        for item in item_list:
            client.send_message(item, msg)


if __name__ == '__main__':
    send_msg_to_tg('test')
