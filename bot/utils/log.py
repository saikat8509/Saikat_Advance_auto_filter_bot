import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE = os.path.join(LOG_DIR, "bot.log")
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 5  # Number of backup log files to keep

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Create logger
logger = logging.getLogger("autofilter_bot")
logger.setLevel(logging.DEBUG)

# Formatter for log messages
formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Rotating file handler to avoid huge logs
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=MAX_LOG_SIZE,
    backupCount=BACKUP_COUNT,
    encoding="utf-8"
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

# Console handler for stdout logging
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def get_logger(name: str = None) -> logging.Logger:
    """
    Returns a logger instance with the given name.
    If no name is provided, returns the root autofilter_bot logger.
    """
    if name:
        return logging.getLogger(f"autofilter_bot.{name}")
    return logger


# Example usage:
# log = get_logger(__name__)
# log.info("Bot started")
