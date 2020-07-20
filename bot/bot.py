import os

from telegram import Update
from telegram.ext import (
    CallbackContext, CommandHandler, ConversationHandler, Dispatcher, Filters,
    MessageHandler, Updater)

from .config import language as cfg
from .decorators import language
from .handlers import remind, start


class ReminderBot:
    def __init__(self, token):
        self._updater = Updater(token, use_context=True)
        self.dispatcher = self._updater.dispatcher

        start_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start.start)],
            states={
                start.CHOOSE_LANG : [CommandHandler('cancel', start.cancel), MessageHandler(Filters.text, start.choose_lang)]
            },
            fallbacks=[]
        )
        self.dispatcher.add_handler(start_handler)

        remind_handler = CommandHandler('remind', remind.remind, pass_args=True, pass_job_queue=True, pass_user_data=True)
        self.dispatcher.add_handler(remind_handler)

        stop_handler = CommandHandler('stop', remind.stop, pass_job_queue=True, pass_user_data=True)
        self.dispatcher.add_handler(stop_handler)

        help_handler = CommandHandler('help', self._help, pass_user_data=True)
        self.dispatcher.add_handler(help_handler)

        self.dispatcher.add_error_handler(self._error)

    def start(self):
        print("{INFO] Starting the bot...")
        self._pool = True
        self._updater.start_polling()


    def stop(self):
        print("[INFO] Stopping the bot...")
        self._pool = False
        self._updater.stop()

    @property
    def pool(self):
        return self._pool

    def _error(self, update : Update, context : CallbackContext):
        print(f"[ERROR] Update from User @{update.effective_user.username} caused error {context.error}")

    @language
    def _help(self, update : Update, context : CallbackContext, lang):
        # get environment variable name connected to HELP response text depending on user's language
        lang_var = cfg.HELP[lang]

        context.bot.send_message(chat_id=update.effective_chat.id, text=os.environ[lang_var], parse_mode='Markdown')