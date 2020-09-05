import os
import signal
import threading

from bot import ReminderBot


def signals_handler(sig, frame):
    print(f"\n[INFO] Stop signal received, stopping the program...")

    bot.stop()
    stop.set()


print("[INFO] press Ctrl+C to stop the program...")
signal.signal(signal.SIGINT, signals_handler)
signal.signal(signal.SIGTERM, signals_handler)

bot = ReminderBot(os.environ["TOKEN"])
bot.start()

stop = threading.Event()

stop.wait()
