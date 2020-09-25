from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler
import os

from ..decorators import make_changes_to
from ..config import language as cfg

CHOOSE_LANG = 0
LOG_LANG_SUCCESS = "[INFO] [START] Setting language to {} for @{}"


def start(update: Update, context: CallbackContext):
    keyboard = ReplyKeyboardMarkup([['English', 'Русский']], one_time_keyboard=True)

    context.bot.send_message(chat_id=update.effective_chat.id, text="Choose your language", reply_markup=keyboard)

    return CHOOSE_LANG


@make_changes_to('language')
def choose_lang(update: Update, context: CallbackContext):
    message = update.message.text

    if message == 'English':
        # Get appropriate response from environment variables
        resp = cfg.START['en']

        context.user_data['language'] = 'en'
        print(LOG_LANG_SUCCESS.format('EN', update.effective_user.username))

    elif message == 'Русский':
        # Get appropriate response from environment variables
        resp = cfg.START['ru']

        context.user_data['language'] = 'ru'
        print(LOG_LANG_SUCCESS.format('RU', update.effective_user.username))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid language, try it again.")
        return

    context.bot.send_message(chat_id=update.effective_chat.id, text=resp, reply_markup=ReplyKeyboardRemove(),
                             parse_mode='MarkdownV2')
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You have canceled the previous command.",
                             reply_markup=ReplyKeyboardRemove)

    return ConversationHandler.END
