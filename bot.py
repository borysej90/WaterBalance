from telegram import Update
from telegram.ext import (
    CallbackContext, CommandHandler, ConversationHandler, Dispatcher, Filters,
    MessageHandler, Updater)

import waterbalanceconfig as cfg
from handlers import start, remind


class ReminderBot:
    CHOOSE_LANG = 0

    def __init__(self, token):
        self._updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        start_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start.start)],
            states={
                ReminderBot.CHOOSE_LANG : [CommandHandler('cancel', start.cancel), MessageHandler(Filters.text, start.choose_lang)]
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
        self.pool = True
        self._updater.start_polling()


    def stop(self):
        print("[INFO] Stopping the bot...")
        self.pool = False
        self._updater.stop()

    @property
    def updater(self):
        return self._updater

    def _error(self, update : Update, context : CallbackContext):
        print(f"[ERROR] Update from User @{update.effective_user.username} caused error {context.error}")

    def _help(self, update : Update, context : CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text=cfg.HELP[context.user_data['lang']], parse_mode='Markdown')
