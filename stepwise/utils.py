import logging
import os


def get_log_level():
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    level = os.getenv("PYTHON_LOG_LEVEL", "DEBUG")
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}, choose one of {valid_levels}")
    return numeric_level

FORMATTER = logging.Formatter(
    "%(asctime)s - %(levelname)-7s - %(name)-25s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
LEVEL = get_log_level()

def configure_custom_logger(level: int = None, formater: logging.Formatter = None):
    global LEVEL, FORMATTER
    if level is not None:
        LEVEL = level
    if formater is not None:
        FORMATTER = formater


def custom_logger(name: str, level: int = None, formatter: logging.Formatter = None):
    if level is None:
        level = LEVEL
    if formatter is None:
        formatter = FORMATTER

    log = logging.getLogger(name)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(level)
    log.handlers = []
    log.addHandler(ch)
    log.setLevel(level)
    return log