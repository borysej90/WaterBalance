import os
import signal
import sys
import time

from bot.bot import ReminderBot


def signals_handler(sig, frame):
    print(f"\n[INFO] Stop signal received, stopping the program...")
    
    bot.stop()
    sys.exit(1)


print("[INFO] press Ctrl+C to stop the program...")
signal.signal(signal.SIGINT, signals_handler)
signal.signal(signal.SIGTERM, signals_handler)

bot = ReminderBot(os.environ["TOKEN"])
bot.start()

while bot.pool:
    time.sleep(1)
