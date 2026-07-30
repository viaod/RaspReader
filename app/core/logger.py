import logging
from datetime import datetime
from functools import wraps
from pathlib import Path

TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")


def log_with_extra(func):
    @wraps(func)
    def wrapper(self, msg, *args, **kwargs):
        extra_info = {}
        for key, value in kwargs.items():
            extra_info[key] = value
        return func(self, msg, *args, extra=extra_info)

    return wrapper


class Logger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.setLevel(logging.DEBUG)
        self.propagate = False

        # Adding a console handler
        console_handler = ConsoleHandler()
        self.addHandler(console_handler)

        # Adding a file handler
        file_handler = CustomFileHandler()
        self.addHandler(file_handler)

    @log_with_extra
    def info(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, msg, args, **kwargs)

    @log_with_extra
    def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.DEBUG):
            self._log(logging.INFO, msg, args, **kwargs)

    @log_with_extra
    def warning(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.WARNING):
            self._log(logging.INFO, msg, args, **kwargs)

    @log_with_extra
    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.ERROR):
            self._log(logging.INFO, msg, args, **kwargs)

    @log_with_extra
    def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.CRITICAL):
            self._log(logging.INFO, msg, args, **kwargs)

    @log_with_extra
    def trace(self, msg, *args, **kwargs):
        if self.isEnabledFor(TRACE_LEVEL):
            self._log(logging.INFO, msg, args, **kwargs)


class ConsoleHandler(logging.StreamHandler):
    def __init__(self, level: int = logging.DEBUG) -> None:
        super().__init__()
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
        )
        self.setFormatter(formatter)
        self.setLevel(level)


class CustomFileHandler(logging.FileHandler):
    def __init__(self):
        log_dir = Path(__file__).resolve().parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / datetime.now().strftime("out_%H_%M_%d_%m_%Y.log")
        super().__init__(log_file, encoding="UTF-8")
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
        )
        self.setFormatter(formatter)
        self.setLevel(logging.INFO)


# Set the custom logger class as the default logger class
logging.setLoggerClass(Logger)

# Use the custom logger
logger = logging.getLogger(__name__)

# Test the overridden methods with extra arguments
# logger.trace("This is a trace log", user_id=123)
# logger.info("This is an info log", user_id=123, task="task1")
# logger.debug("This is a debug log", user_id=123)
# logger.warning("This is a warning log", user_id=456, context="example")
# logger.error("This is an error log", error_code=500, details="Internal Server Error")
# logger.critical("This is a critical log", user_id=789, action="shutdown")
