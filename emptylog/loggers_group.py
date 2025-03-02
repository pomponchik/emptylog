import sys
from typing import Tuple, Callable, Any
from threading import Lock
from collections.abc import Iterator

from printo import descript_data_object

from emptylog.protocols import LoggerProtocol, LoggerMethodProtocol
from emptylog.abstract_logger import AbstractLogger


if sys.version_info < (3, 9):
    GroupIterator = Iterator  # pragma: no cover
else:
    GroupIterator = Iterator[LoggerProtocol]  # pragma: no cover

class LoggersGroup(AbstractLogger):
    loggers: Tuple[LoggerProtocol, ...]

    def __init__(self, *loggers: LoggerProtocol) -> None:
        for logger in loggers:
            if not isinstance(logger, LoggerProtocol):
                raise TypeError(f'A logger group can only be created from loggers. You passed {repr(logger)} ({type(logger).__name__}).')

        self.loggers = loggers
        self.lock = Lock()

    def __repr__(self) -> str:
        return descript_data_object(type(self).__name__, self.loggers, {})

    def __len__(self) -> int:
        return len(self.loggers)

    def __iter__(self) -> GroupIterator:  # type: ignore[type-arg, unused-ignore]
        yield from self.loggers

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
