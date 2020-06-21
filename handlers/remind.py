from telegram import Update
from telegram.ext import CallbackContext
import os

from decorators import language

import languagecfg as cfg


@language
def remind(update : Update, context : CallbackContext, lang):
    if not context.args:
        due = 30
    else:
        due = float(context.args[0])

    if 'job' in context.user_data:
        context.user_data['job'].schedule_removal()

    if 'last_remind' not in context.user_data:
        context.user_data['last_remind'] = []
    
    # get environment variable name connected to REMIND response text depending on user's language
    lang_var = cfg.REMIND[lang]

    context.bot.send_message(chat_id=update.effective_chat.id, text=os.environ[lang_var].format(due))
    
    # convert interval into seconds
    due *= 60

    # Job context contains ChatId related to the job, last remind message id (or empty list) and user's language
    job_context = (update.effective_chat.id, context.user_data['last_remind'], lang)

    context.user_data['job'] = context.job_queue.run_repeating(_drink, due, context=job_context)

def _drink(context : CallbackContext):
    job = context.job

    chat_id, last_remind_msg, lang = job.context

    # get environment variable name connected to DRINK response text depending on user's language
    lang_var = cfg.DRINK[lang]

    # job.context contains (chat_id, last_remind_msg_id, user_lang)
    message = context.bot.send_message(chat_id=chat_id, text=os.environ[lang_var])

    if len(last_remind_msg) > 0:
        # job.context[1] is a list where the first (and the only) element is last remind msg ID
        context.bot.delete_message(chat_id=chat_id, message_id=last_remind_msg[0])

        # replace last remind message id with new (actual) one
        last_remind_msg[0] = message.message_id
    else:
        last_remind_msg.append(message.message_id)

@language
def stop(update : Update, context : CallbackContext, lang):
    if 'job' not in context.user_data:
        # get environment variable name connected to STOP_NOT_EXIST response text depending on user's language
        lang_var = cfg.STOP_NOT_EXiST[lang]

        context.bot.send_message(chat_id=update.effective_chat.id, text=os.environ[lang_var])
        return
    
    context.user_data['job'].schedule_removal()
    del context.user_data['job']

    # get environment variable name connected to STOP response text depending on user's language
    lang_var = cfg.STOP[lang]

    context.bot.send_message(chat_id=update.effective_chat.id, text=os.environ[lang_var])
