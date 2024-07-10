from abc import ABC

from emptylog.protocols import LoggerProtocol


class AbstractLogger(LoggerProtocol, ABC):
    def __repr__(self) -> str:
        return f'{type(self).__name__}()'
    
    def __add__(self, other: LoggerProtocol) -> 'LoggersGroup':  # type: ignore[name-defined] # noqa: F821
        if not isinstance(other, LoggerProtocol):
            raise NotImplementedError('The addition operation is defined only for loggers.')

        from emptylog import LoggersGroup

        return LoggersGroup(self, other)

    def __radd__(self, other: LoggerProtocol) -> 'LoggersGroup':  # type: ignore[name-defined] # noqa: F821
        if not isinstance(other, LoggerProtocol):
            raise NotImplementedError('The addition operation is defined only for loggers.')

        from emptylog import LoggersGroup

        return LoggersGroup(other, self)
