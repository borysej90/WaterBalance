import os

from .config import language as cfg


def language(func):
    def wrapper(*args, **kwargs):
        update = args[-2]
        context = args[-1]

        if 'language' in context.user_data:
            return func(*args)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Sorry, I don't know your language.\nPlease type /start")

    return wrapper


def time_format(func):
    def wrapper(*args, **kwargs):
        update = args[-2]
        context = args[-1]

        message = update.message.text

        time = message.split(':')
        time = [*map(int, time)]

        time_correct = -1 < time[0] < 25

        if len(time) > 1:
            time_correct = time_correct and -1 < time[1] < 60

        if time_correct:
            return func(*args)
        else:
            lang = context.user_data['language']

            # get TIME_FORMAT_ERROR environment variable name
            lang_var = cfg.TIME_FORMAT_ERROR[lang]

            context.bot.send_message(chat_id=update.effective_chat.id, text=os.environ[lang_var], parse_mode='Markdown')

            return

    return wrapper
