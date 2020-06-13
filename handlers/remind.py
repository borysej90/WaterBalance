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

    # get user's lang
    lang = context.user_data['lang']

    if 'last_remind' not in context.user_data:
        context.user_data['last_remind'] = []

    context.bot.send_message(chat_id=update.effective_chat.id, text=cfg.REMIND[lang].format(due))
    
    # convert interval into seconds
    due *= 60

    context.user_data['job'] = context.job_queue.run_repeating(_drink, due,
                                            context=(update.effective_chat.id, context.user_data['last_remind'], lang))

def _drink(context : CallbackContext):
    job = context.job

    # job.context contains (chat_id, last_remind_msg_id, user_lang)
    message = context.bot.send_message(chat_id=job.context[0], text=cfg.DRINK[job.context[2]])

    if len(job.context[1]) > 0:
        # job.context[1] is a list where the first (and the only) element is last remind msg ID
        context.bot.delete_message(chat_id=job.context[0], message_id=job.context[1][0])
        job.context[1][0] = message.message_id
    else:
        job.context[1].append(message.message_id)

def stop(update : Update, context : CallbackContext):
    if 'job' not in context.user_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text=cfg.STOP_NOT_EXiST[context.user_data['lang']])
        return
    
    context.user_data['job'].schedule_removal()
    del context.user_data['job']

    context.bot.send_message(chat_id=update.effective_chat.id, text=cfg.STOP[context.user_data['lang']])
