import datetime
import os

from telegram import Update
from telegram.ext import CallbackContext

from ..config import language as cfg
from ..decorators import language


@language
def remind(update : Update, context : CallbackContext):
    if not context.args:
        due = 30.
    else:
        due = float(context.args[0])

    if 'job' in context.user_data:
        context.user_data['job'].schedule_removal()

    if 'last_remind' not in context.user_data:
        context.user_data['last_remind'] = []

    lang = context.user_data['lang']
    
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

    if 'silence_start' in context.user_data:
        delta = datetime.timedelta(seconds=job.interval)
        if datetime.datetime.utcnow().time() + delta >= context.user_data['silence_start']:
            # remove current Job from Job queue
            context.user_data['job'].schedule_removal()

            # define when send message after Silence ends
            first = context.user_data['silence_end'] + delta

            # create new interval Job after Silence period
            context.user_data['job'] = context.job_queue.run_repeating(_drink, interval=job.interval, first=first, context=job.context)
            return

    chat_id, last_remind_msg, lang = job.context

    # get environment variable name connected to DRINK response text depending on user's language
    lang_var = cfg.DRINK[lang]

    # job.context contains (chat_id, last_remind_msg_id, user_lang)
    message = context.bot.send_message(chat_id=chat_id, text=os.environ[lang_var])

    # Check if list contains last remind message id
    if len(last_remind_msg) > 0:
        # job.context[1] is a list where the first (and the only) element is last remind msg ID
        context.bot.delete_message(chat_id=chat_id, message_id=last_remind_msg[0])

        # replace last remind message id with new (actual) one
        last_remind_msg[0] = message.message_id
    # if not, add latest remind message id to it
    else:
        last_remind_msg.append(message.message_id)

@language
def stop(update : Update, context : CallbackContext):
    lang = context.user_data['lang']
    
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


# def _get_timezone(tz_offset, common_only=True):
#     # pick one of the timezone collections
#     timezones = pytz.common_timezones if common_only else pytz.all_timezones

#     # convert the float hours offset to a timedelta
#     offset_days, offset_seconds = 0, int(tz_offset * 3600)
#     if offset_seconds < 0:
#         offset_days = -1
#         offset_seconds += 24 * 3600
#     desired_delta = datetime.timedelta(offset_days, offset_seconds)

#     # Loop through the timezones and find any with matching offsets
#     null_delta = datetime.timedelta(0, 0)
#     result = ''
#     for tz_name in timezones:
#         tz = pytz.timezone(tz_name)
#         non_dst_offset = getattr(tz, '_transition_info', [[null_delta]])[-1]
#         if desired_delta == non_dst_offset[0]:
#             result = tz_name
#             break

#     result = pytz.timezone(result)

#     return result
