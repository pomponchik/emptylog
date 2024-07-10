from typing import Callable, Any
from datetime import datetime
from functools import partial

from emptylog.abstract_logger import AbstractLogger


class PrintingLogger(AbstractLogger):
    def __init__(self, printing_callback: Callable[[Any], Any] = partial(print, end=''), separator: str = '|') -> None:
        self.callback = printing_callback
        self.separator = separator
        self.template = '{time} {separator} {level} {separator} {message}\n'

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.callback(self.create_line('DEBUG', message))

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.callback(self.create_line('INFO', message))

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.callback(self.create_line('WARNING', message))

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.callback(self.create_line('ERROR', message))

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.callback(self.create_line('EXCEPTION', message))

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.callback(self.create_line('CRITICAL', message))

    def create_line(self, level: str, message: str) -> str:
        return self.template.format(time=datetime.now(), level=level.ljust(9), message=message, separator=self.separator)
