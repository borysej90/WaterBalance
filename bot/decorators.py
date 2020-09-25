import os
import functools

from .config import language as cfg


def language(func):
    @functools.wraps(func)
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
    @functools.wraps(func)
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

            # get connected to TIME_FORMAT_ERROR response text depending on user's language
            lang_var = cfg.TIME_FORMAT_ERROR[lang]

            context.bot.send_message(chat_id=update.effective_chat.id, text=lang_var, parse_mode='Markdown')

            return

    return wrapper


def make_changes_to(field):
    """
    Marks that function made changes to `user_data`.
    """
    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            context = args[-1]

            old_value = context.user_data.get(field, None)

            ret = func(*args, **kwargs)

            if old_value != context.user_data.get(field, None):
                context.user_data['changed'] = True

            return ret

        return wrapper

    return inner
