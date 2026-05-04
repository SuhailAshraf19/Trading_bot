import logging
from config import LOG_TO_FILE

if LOG_TO_FILE:
    logging.basicConfig(
        filename="bot.log",
        level=logging.INFO,
        format="%(asctime)s - %(message)s"
    )

def log(msg):
    print(msg)
    if LOG_TO_FILE:
        logging.info(msg)