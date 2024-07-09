from typing import Any

from emptylog.abstract_logger import AbstractLogger
from emptylog.call_data import LoggerCallData
from emptylog.accumulated_data import LoggerAccumulatedData


class MemoryLogger(AbstractLogger):
    def __init__(self) -> None:
        self.data = LoggerAccumulatedData()

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None: self.data.debug.append(LoggerCallData(message, args, kwargs))
    def info(self, message: str, *args: Any, **kwargs: Any) -> None: self.data.info.append(LoggerCallData(message, args, kwargs))
    def warning(self, message: str, *args: Any, **kwargs: Any) -> None: self.data.warning.append(LoggerCallData(message, args, kwargs))
    def error(self, message: str, *args: Any, **kwargs: Any) -> None: self.data.error.append(LoggerCallData(message, args, kwargs))
    def exception(self, message: str, *args: Any, **kwargs: Any) -> None: self.data.exception.append(LoggerCallData(message, args, kwargs))
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None: self.data.critical.append(LoggerCallData(message, args, kwargs))
