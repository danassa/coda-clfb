from general.constants import *
import logging
import configparser
from general.gui import create_gui

logFormatter = logging.Formatter("%(asctime)s %(levelname)s:%(funcName)s %(message)s")
fileHandler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8')
fileHandler.setFormatter(logFormatter)
streamHandler = logging.StreamHandler()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

logging.info('Starting C.L.F.B Tool..')

try:
    logging.info('Reading configuration')
    config = configparser.ConfigParser()
    config.read(CONF_FILE)
    max_chars = config['default'].getint('max_chars', fallback=MAX_CHARS_PER_VOLUME)
    min_chars = config['default'].getint('min_chars', fallback=MIN_CHARS_PER_VOLUME)
    log_level = config['default'].get('log_level', fallback="INFO")
except Exception as e:
    logging.exception(e)
    logging.info('falling to default configuration')
    max_chars = MAX_CHARS_PER_VOLUME
    min_chars = MIN_CHARS_PER_VOLUME
    log_level = "INFO"

logger.setLevel(log_level)

create_gui(max_chars, min_chars)
