import logging
import sys

# Log Levels
# ----------
# debug - 10
# info - 20
# warning - 30
# error - 40
# critical - 50

FORMAT = "%(asctime)s — %(name)s — %(levelname)s — [ %(filename)s:%(lineno)s ] - %(message)s"

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(FORMAT)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = 0
    logger.setLevel(logging.DEBUG) # better to have too much log than not enough
    return logger