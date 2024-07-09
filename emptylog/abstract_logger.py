from abc import ABC

from emptylog.protocol import LoggerProtocol


class AbstractLogger(LoggerProtocol, ABC):
    def __add__(self, other: LoggerProtocol) -> 'LoggersGroup':
        if not isinstance(other, LoggerProtocol):
            raise NotImplementedError('The addition operation is defined only for loggers.')

        from emptylog import LoggersGroup

        return LoggersGroup(self, other)
