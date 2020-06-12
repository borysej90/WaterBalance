from telegram.ext import Updater, Dispatcher, CallbackContext, Filters
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
import waterbalanceconfig as cfg

class ReminderBot:
    CHOOSE_LANG = 0

    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        cancel_handler = CommandHandler('cancel', self._cancel_converstation)

        start_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self._start)],
            states={
                ReminderBot.CHOOSE_LANG : [cancel_handler, MessageHandler(Filters.text, self._choose_lang)]
            },
            fallbacks=[]
        )
        self.dispatcher.add_handler(start_handler)

    def start(self):
        print("{INFO] Starting the bot...")
        self.updater.start_polling()


    def stop(self):
        print("[INFO] Stopping the bot...")
        self.updater.stop()

    def _start(self, update : Update, context : CallbackContext):
        keyboard = ReplyKeyboardMarkup([['English', 'Русский']], one_time_keyboard=True)

        context.bot.send_message(chat_id=update.effective_chat.id, text="Choose your language", reply_markup=keyboard)

        return ReminderBot.CHOOSE_LANG
    
    def _choose_lang(self, update : Update, context : CallbackContext):
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

    def _cancel_converstation(self, update : Update, context : CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="You have canceled the previous command.")
        return ConversationHandler.END
    