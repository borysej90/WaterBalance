import os
import signal
import sys
import time

from bot.bot import ReminderBot


def signals_handler(sig, frame):
    print(f"[INFO] Signal {sig} received, stopping the program...")
    
    bot.stop()

print("[INFO] press Ctrl+C to stop the program...")
signal.signal(signal.SIGINT | signal.SIGTERM, signals_handler)

bot = ReminderBot(os.environ["TOKEN"])
bot.start()

while bot.pool:
    time.sleep(1)
