import signal
import sys
from multiprocessing import Process
from time import sleep

import waterbalanceconfig as cfg
from bot import ReminderBot


def signals_handler(sig, frame):
    print("[INFO] You have pressed `Ctrl + C`, stopping the program...")
    
    bot.stop()

print("[INFO] press Ctrl+C to stop the program...")
signal.signal(signal.SIGINT, signals_handler)

bot = ReminderBot(cfg.TOKEN)
bot.start()

while bot.pool:
    sleep(1)
