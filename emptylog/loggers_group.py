from typing import Tuple, Callable, Any
from threading import Lock

from printo import descript_data_object

from emptylog.protocols import LoggerProtocol, LoggerMethodProtocol
from emptylog.abstract_logger import AbstractLogger


class LoggersGroup(AbstractLogger):
    loggers: Tuple[LoggerProtocol, ...]

    def __init__(self, *loggers: LoggerProtocol) -> None:
        self.loggers = loggers
        self.lock = Lock()

    def __repr__(self) -> str:
        return descript_data_object(type(self).__name__, self.loggers, {}, serializator=repr)

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.run_loggers(lambda x: x.debug, message, *args, **kwargs)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.run_loggers(lambda x: x.info, message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.run_loggers(lambda x: x.warning, message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.run_loggers(lambda x: x.error, message, *args, **kwargs)

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.run_loggers(lambda x: x.exception, message, *args, **kwargs)

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.run_loggers(lambda x: x.critical, message, *args, **kwargs)

    def run_loggers(self, get_method: Callable[[LoggerProtocol], LoggerMethodProtocol], message: str, *args: Any, **kwargs: Any) -> None:
        with self.lock:
            for logger in self.loggers:
                method = get_method(logger)
                method(message, *args, **kwargs)
