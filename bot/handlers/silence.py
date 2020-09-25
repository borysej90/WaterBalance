import datetime
import os

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from ..config import language as cfg
from ..decorators import make_changes_to, language, time_format

SET_TIMEZONE, SET_START, SET_END = range(0, 3)
START, END = "start", "end"


@language
def silence(update: Update, context: CallbackContext):
    lang = context.user_data['language']

    # get connected to CALIBRATION response text depending on user's language
    lang_var = cfg.CALIBRATION[lang]

    context.bot.send_message(chat_id=update.effective_chat.id, text=lang_var, parse_mode='MarkdownV2')

    return SET_TIMEZONE


@make_changes_to('timezone')
def set_timezone(update: Update, context: CallbackContext):
    lang = context.user_data['language']

    try:
        user_hour = int(update.effective_message.text)
    except ValueError:
        # get connected to TIMEZONE_ERROR response text depending on user's language
        lang_var = cfg.TIMEZONE_ERROR[lang]

        context.bot.send_message(chat_id=update.effective_chat.id, text=lang_var, parse_mode='MarkdownV2')
        return

    # check if user sent wrong time zone
    if user_hour > 23 or user_hour < 0:
        # get connected to TIMEZONE_ERROR response text depending on user's language
        lang_var = cfg.TIMEZONE_ERROR[lang]

        context.bot.send_message(chat_id=update.effective_chat.id, text=lang_var, parse_mode='MarkdownV2')
        return

    curr_hour = datetime.datetime.utcnow().hour

    context.user_data['timezone'] = user_hour - curr_hour

    # get connected to TIMEZONE_OK response text depending on user's language
    lang_var = cfg.TIMEZONE_OK[lang]

    context.bot.send_message(chat_id=update.effective_chat.id, text=lang_var, parse_mode='MarkdownV2')

    return SET_START


@time_format
@make_changes_to('start_silence')
def set_start(update: Update, context: CallbackContext):
    lang = context.user_data['language']

    _set_boundary(update, context, START)

    # get connected to START_SILENCE response text depending on user's language
    lang_var = cfg.START_SILENCE[lang]

    context.bot.send_message(chat_id=update.effective_chat.id, text=lang_var, parse_mode='MarkdownV2')

    return SET_END


@time_format
@make_changes_to('end_silence')
def set_end(update: Update, context: CallbackContext):
    lang = context.user_data['language']

    _set_boundary(update, context, END)

    # get connected to END_SILENCE response text depending on user's language
    lang_var = cfg.END_SILENCE[lang]

    context.bot.send_message(chat_id=update.effective_chat.id, text=lang_var, parse_mode='MarkdownV2')

    return ConversationHandler.END


def _set_boundary(update: Update, context: CallbackContext, boundary):
    message = update.message.text

    # get hours and minutes from user's message
    time = message.split(':')

    # convert to integers
    time = [*map(int, time)]

    # if only hours passed than add 0 minutes
    if len(time) == 1:
        time.append(0)

    delta = context.user_data['timezone']

    context.user_data[f'{boundary}_silence'] = datetime.time(time[0] - delta, time[1])


@language
def cancel(update: Update, context: CallbackContext):
    lang = context.user_data['language']

    # get connected to CANCEL response text depending on user's language
    lang_var = cfg.CANCEL[lang]

    context.bot.send_message(chat_id=update.effective_chat.id, text=lang_var)

    return ConversationHandler.END
