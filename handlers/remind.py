from telegram import Update
from telegram.ext import CallbackContext

import waterbalanceconfig as cfg


def remind(update : Update, context : CallbackContext):
    if not context.args:
        due = 30
    else:
        due = int(context.args[0])

    if 'job' in context.user_data:
        context.user_data['job'].schedule_removal()

    lang = context.user_data['lang']

    context.bot.send_message(chat_id=update.effective_chat.id, text=cfg.REMIND[lang].format(due))
    
    due *= 60

    context.user_data['job'] = context.job_queue.run_repeating(_drink, due, context=(update.effective_chat.id, lang))

def _drink(context : CallbackContext):
    job = context.job

    context.bot.send_message(chat_id=job.context[0], text=cfg.DRINK[job.context[1]])

def stop(update : Update, context : CallbackContext):
    if 'job' not in context.user_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text=cfg.STOP_NOT_EXiST[context.user_data['lang']])
        return
    
    context.user_data['job'].schedule_removal()
    del context.user_data['job']

    context.bot.send_message(chat_id=update.effective_chat.id, text=cfg.STOP[context.user_data['lang']])
