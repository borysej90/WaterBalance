from telegram import Update
from telegram.ext import CallbackContext

from decorators import language

import waterbalanceconfig as cfg


@language
def remind(update : Update, context : CallbackContext, lang):
    if not context.args:
        due = 30
    else:
        due = int(context.args[0])

    if 'job' in context.user_data:
        context.user_data['job'].schedule_removal()

    # get user's lang
    lang = context.user_data['lang']

    if 'last_remind' not in context.user_data:
        context.user_data['last_remind'] = []

    context.bot.send_message(chat_id=update.effective_chat.id, text=cfg.REMIND[lang].format(due))
    
    # convert interval into seconds
    due *= 60

    # Job context contains ChatId related to the job, last remind message id (or empty list) and user's language
    # 
    job_context = (update.effective_chat.id, context.user_data['last_remind'], lang)

    context.user_data['job'] = context.job_queue.run_repeating(_drink, due, context=job_context)

def _drink(context : CallbackContext):
    job = context.job

    chat_id, last_remind_msg_id, lang = job.context


    # job.context contains (chat_id, last_remind_msg_id, user_lang)
    message = context.bot.send_message(chat_id=chat_id, text=cfg.DRINK[lang])

    if len(job.context[1]) > 0:
        # job.context[1] is a list where the first (and the only) element is last remind msg ID
        context.bot.delete_message(chat_id=chat_id, message_id=last_remind_msg_id)

        # replace last remind message id with new (actual) one
        last_remind_msg_id = message.message_id
    else:
        last_remind_msg_id.append(message.message_id)

@language
def stop(update : Update, context : CallbackContext, lang):
    if 'job' not in context.user_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text=cfg.STOP_NOT_EXiST[lang])
        return
    
    context.user_data['job'].schedule_removal()
    del context.user_data['job']

    context.bot.send_message(chat_id=update.effective_chat.id, text=cfg.STOP[lang])
