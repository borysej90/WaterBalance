import datetime
import os

from telegram import Update
from telegram.ext import CallbackContext

from ..config import language as cfg
from ..decorators import make_changes_to, language


@language
@make_changes_to('job')
def remind(update: Update, context: CallbackContext):
    if not context.args:
        due = 30.
    else:
        due = float(context.args[0])

    if 'job' in context.user_data:
        context.user_data['job'].schedule_removal()

    lang = context.user_data['language']

    # get connected to REMIND response text depending on user's language
    lang_var = cfg.REMIND[lang]

    context.bot.send_message(chat_id=update.effective_chat.id, text=lang_var.format(due))

    # convert interval into seconds
    due *= 60

    # Job context will be accessed in Job callback and contains:
    # [+] ChatID
    # [+] User data dict
    job_context = (update.effective_chat.id, context.user_data)

    context.user_data['job'] = context.job_queue.run_repeating(_drink, due, context=job_context)


def _drink(context: CallbackContext):
    job = context.job

    # job.context contains (chat_id, last_remind_msg_id, user_data)
    chat_id, user_data = job.context

    is_silence = False
    if {'start_silence', 'end_silence'} <= set(user_data):
        is_silence = _check_silence(user_data['start_silence'], user_data['end_silence'], job.interval)

    if is_silence:
        # remove current Job from Job queue
        user_data['job'].schedule_removal()

        # get silence_end boundary
        end = user_data['end_silence']

        delta = datetime.timedelta(seconds=job.interval)

        # define when send first message after Silence ends
        # NOTE: year, month and day do not matter here
        first = (datetime.datetime(2000, 1, 1, end.hour, end.minute) + delta).time()

        # create new interval Job after Silence period
        user_data['job'] = context.job_queue.run_repeating(_drink, interval=job.interval, first=first,
                                                           context=job.context)
        return

    lang = user_data['language']

    # get connected to DRINK response text depending on user's language
    lang_var = cfg.DRINK[lang]

    message = context.bot.send_message(chat_id=chat_id, text=lang_var)

    # Check if user_data contains last remind message id
    if 'last_remind' in user_data:
        context.bot.delete_message(chat_id=chat_id, message_id=user_data['last_remind'])

    # create or replace last remind message id with new (actual) one
    user_data['last_remind'] = message.message_id


def _check_silence(start, end: datetime.time, step: int):
    """
    Checks whether current time + `step` (in seconds) is in silence period.

    Args:
         start (datetime.time): Start of silence period.
         end (datetime.time): End of silence period.
         step (int): How many seconds from now.

    Returns:
        bool: True if in silence period, otherwise False.
    """

    delta = datetime.timedelta(seconds=step)

    # get time of next potential reminding
    next_reminding = (datetime.datetime.utcnow() + delta).time()

    # check if next reminding violates silence_start boundary
    is_silence = next_reminding >= start

    # this if-clause check if boundaries are in the same day, e.g. 12:00-16:00
    # then we have to check also if we violate silence_end boundary
    if start < end:
        is_silence = is_silence and next_reminding <= end

    return is_silence


@language
@make_changes_to('job')
def stop(update: Update, context: CallbackContext):
    lang = context.user_data['language']

    if 'job' not in context.user_data:
        # get  connected to STOP_NOT_EXIST response text depending on user's language
        lang_var = cfg.STOP_NOT_EXiST[lang]

        context.bot.send_message(chat_id=update.effective_chat.id, text=lang_var)
        return

    context.user_data['job'].schedule_removal()
    del context.user_data['job']

    # get connected to STOP response text depending on user's language
    lang_var = cfg.STOP[lang]

    context.bot.send_message(chat_id=update.effective_chat.id, text=lang_var)