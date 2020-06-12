from telegram.ext import Updater, Dispatcher, Filters
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler

import waterbalanceconfig as cfg

from handlers import start

class ReminderBot:
    CHOOSE_LANG = 0

    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        start_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self._start)],
            states={
                ReminderBot.CHOOSE_LANG : [CommandHandler('cancel', start.cancel), MessageHandler(Filters.text, self._choose_lang)]
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