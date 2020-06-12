from telegram import Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler

import waterbalanceconfig as cfg

CHOOSE_LANG = 0

def start(update : Update, context : CallbackContext):
    keyboard = ReplyKeyboardMarkup([['English', 'Русский']], one_time_keyboard=True)

    context.bot.send_message(chat_id=update.effective_chat.id, text="Choose your language", reply_markup=keyboard)

    return CHOOSE_LANG

def choose_lang(update : Update, context : CallbackContext):
    message = update.message.text

    if message == 'English':
        resp = cfg.START_EN
        context.user_data['lang'] = 'en'
        print(f"[U:{update.effective_user.username}] Setting language to EN")
    elif message == 'Русский':
        resp = cfg.START_RU
        context.user_data['lang'] = 'ru'
        print(f"[U:{update.effective_user.username}] Setting language to RU")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid language, try it again.")
        return

    context.bot.send_message(chat_id=update.effective_chat.id, text=resp, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
    return ConversationHandler.END

def cancel(update : Update, context : CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You have canceled the previous command.", 
                            reply_markup=ReplyKeyboardRemove)
                            
    return ConversationHandler.END
