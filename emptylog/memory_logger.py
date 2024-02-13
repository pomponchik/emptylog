from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any

from emptylog.protocol import LoggerProtocol


@dataclass
class LoggerCallData:
    message: str
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]


@dataclass
class LoggerAccumulatedData:
    debug: List[LoggerCallData] = field(default_factory=list)
    info: List[LoggerCallData] = field(default_factory=list)
    warning: List[LoggerCallData] = field(default_factory=list)
    error: List[LoggerCallData] = field(default_factory=list)
    exception: List[LoggerCallData] = field(default_factory=list)
    critical: List[LoggerCallData] = field(default_factory=list)


class MemoryLogger(LoggerProtocol):
    def __init__(self) -> None:
        self.data = LoggerAccumulatedData()

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None: self.data.debug.append(LoggerCallData(message, args, kwargs))
    def info(self, message: str, *args: Any, **kwargs: Any) -> None: self.data.info.append(LoggerCallData(message, args, kwargs))
    def warning(self, message: str, *args: Any, **kwargs: Any) -> None: self.data.warning.append(LoggerCallData(message, args, kwargs))
    def error(self, message: str, *args: Any, **kwargs: Any) -> None: self.data.error.append(LoggerCallData(message, args, kwargs))
    def exception(self, message: str, *args: Any, **kwargs: Any) -> None: self.data.exception.append(LoggerCallData(message, args, kwargs))
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None: self.data.critical.append(LoggerCallData(message, args, kwargs))
