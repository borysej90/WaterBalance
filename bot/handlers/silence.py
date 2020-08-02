from datetime import datetime
import os

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from ..config import language as cfg
from ..decorators import language, time_format

SET_TIMEZONE, SET_START, SET_END = range(0, 3)

@language
def silence(update: Update, context: CallbackContext):
    lang = context.user_data['lang']

    # get CALIBRATION environment variable name
    lang_var = cfg.CALIBRATION[lang]

    context.bot.send_message(chat_id=update.effective_chat.id, text=os.environ[lang_var], parse_mode='Markdown')

    return SET_TIMEZONE

def set_timezone(update: Update, context: CallbackContext):
    lang = context.user_data['lang']

    try:
        user_hour = int(update.effective_message.text)
    except ValueError:
        # get TIMEZONE_ERROR_RESP environment variable name
        lang_var = cfg.TIMEZONE_ERROR[lang]

        context.bot.send_message(chat_id=update.effective_chat.id, text=os.environ[lang_var], parse_mode='Markdown')
        return

    # check if user sent wrong time zone
    if user_hour > 13 or user_hour < -12:
        # get TIMEZONE_ERROR environment variable name
        lang_var = cfg.TIMEZONE_ERROR[lang]

        context.bot.send_message(chat_id=update.effective_chat.id, text=os.environ[lang_var], parse_mode='Markdown')
        return

    curr_hour = datetime.utcnow().hour

    context.user_data['timezone'] = user_hour - curr_hour

    # get TIMEZONE_OK environment variable name
    lang_var = cfg.TIMEZONE_OK[lang]

    context.bot.send_message(chat_id=update.effective_chat.id, text=os.environ[lang_var], parse_mode='Markdown')

    return SET_START

@time_format
def set_start(update: Update, context: CallbackContext):
    lang = context.user_data['lang']

    message = update.message.text

    context.user_data['silence_start'] = message.split(':')

    # get START_SILENCE environment variable name
    lang_var = cfg.START_SILENCE[lang]

    context.bot.send_message(chat_id=update.effective_chat.id, text=os.environ[lang_var])

    return SET_END

@time_format
def set_end(update: Update, context: CallbackContext):
    lang = context.user_data['lang']

    message = update.message.text

    context.user_data['silence_end'] = message.split(':')

    # get START_SILENCE environment variable name
    lang_var = cfg.END_SILENCE[lang]

    context.bot.send_message(chat_id=update.effective_chat.id, text=os.environ[lang_var])

    return ConversationHandler.END

@language
def cancel(update : Update, context : CallbackContext):
    lang = context.user_data['lang']

    # get CANCEL environment variable name
    lang_var = cfg.CANCEL[lang]

    if context.user_data['timezone']:
        del context.user_data['timezone']

    if context.user_data['silence_start']:
        del context.user_data['silence_start']

    context.bot.send_message(chat_id=update.effective_chat.id, text=os.environ[lang_var])
                            
    return ConversationHandler.END