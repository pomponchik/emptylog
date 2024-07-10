from abc import ABC

from emptylog.protocols import LoggerProtocol


class AbstractLogger(LoggerProtocol, ABC):
    def __repr__(self) -> str:
        return f'{type(self).__name__}()'

    def __add__(self, other: LoggerProtocol) -> 'LoggersGroup':  # type: ignore[name-defined] # noqa: F821
        if not isinstance(other, LoggerProtocol):
            raise NotImplementedError('The addition operation is defined only for loggers.')

        from emptylog import LoggersGroup

        local_loggers = self.loggers if isinstance(self, LoggersGroup) else [self]
        other_loggers = other.loggers if isinstance(other, LoggersGroup) else [other]

        return LoggersGroup(*local_loggers, *other_loggers)

    def __radd__(self, other: LoggerProtocol) -> 'LoggersGroup':  # type: ignore[name-defined] # noqa: F821
        if not isinstance(other, LoggerProtocol):
            raise NotImplementedError('The addition operation is defined only for loggers.')

        from emptylog import LoggersGroup

        local_loggers = self.loggers if isinstance(self, LoggersGroup) else [self]
        other_loggers = other.loggers if isinstance(other, LoggersGroup) else [other]

        return LoggersGroup(*other_loggers, *local_loggers)
