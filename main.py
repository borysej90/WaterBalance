import waterbalanceconfig as cfg
from bot import ReminderBot


import signal
import sys
from multiprocessing import Process
from time import sleep

def main():
    def signals_handler(sig, frame):
        nonlocal bot
        print("[INFO] You have pressed Ctrl+C, stopping the bot...")

        bot.updater.stop()
        print("Done")

        sys.exit()


    print("[INFO] press Ctrl+C to stop the program...")
    signal.signal(signal.SIGINT, signals_handler)

    bot = ReminderBot(cfg.TOKEN)
    bot.start()

    while True:
        sleep(1)

if __name__ == "__main__":
    main()