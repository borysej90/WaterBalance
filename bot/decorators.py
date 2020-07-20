from telegram.ext import CallbackContext
from telegram import Update

def language(func):
    def wrapper(*args):
        update = args[0]
        context = args[1]

        if 'lang' in context.user_data:            
            return func(update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I don't know your language.\nPlease type /start")
    
    return wrapper