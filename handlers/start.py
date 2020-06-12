from telegram.ext import CallbackContext
from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove

def start(self, update : Update, context : CallbackContext):
        keyboard = ReplyKeyboardMarkup([['English', 'Русский']], one_time_keyboard=True)

        context.bot.send_message(chat_id=update.effective_chat.id, text="Choose your language", reply_markup=keyboard)

        return ReminderBot.CHOOSE_LANG

def choose_lang(self, update : Update, context : CallbackContext):
    message = update.message.text

    if message == 'English':
        resp = cfg.START_EN
        context.user_data['lang'] = 'en'
    elif message == 'Русский':
        resp = cfg.START_RU
        context.user_data['lang'] = 'ru'
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Choose your language again")
        return

    context.bot.send_message(chat_id=update.effective_chat.id, text=resp)
    return ConversationHandler.END

def cancel(self, update : Update, context : CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You have canceled the previous command.")
    return ConversationHandler.END