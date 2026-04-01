import logging

from loguru import logger as loguru_logger

from emptylog import (
    EmptyLogger,
    LoggerProtocol,
    LoggersGroup,
    MemoryLogger,
    PrintingLogger,
)


def test_positive_examples_of_runtime_check():
    assert isinstance(logging, LoggerProtocol)
    assert isinstance(logging.getLogger('kek'), LoggerProtocol)
    assert isinstance(logging.getLogger('lol'), LoggerProtocol)
    assert isinstance(EmptyLogger(), LoggerProtocol)
    assert isinstance(LoggersGroup(), LoggerProtocol)
    assert isinstance(MemoryLogger(), LoggerProtocol)
    assert isinstance(PrintingLogger(), LoggerProtocol)


def test_negative_examples_of_runtime_check():
    assert not isinstance(1, LoggerProtocol)
    assert not isinstance('logging', LoggerProtocol)


def test_loguru_logger_is_logger():
    assert isinstance(loguru_logger, LoggerProtocol)


def test_object_missing_one_method_is_not_logger():
    class AlmostLogger:
        def debug(self, message, *args, **kwargs): pass
        def info(self, message, *args, **kwargs): pass
        def warning(self, message, *args, **kwargs): pass
        def error(self, message, *args, **kwargs): pass
        def exception(self, message, *args, **kwargs): pass
        # no critical

    assert not isinstance(AlmostLogger(), LoggerProtocol)


def test_runtime_check_does_not_verify_method_signature():
    class WrongSignatureLogger:
        def debug(self): pass
        def info(self): pass
        def warning(self): pass
        def error(self): pass
        def exception(self): pass
        def critical(self): pass

    assert isinstance(WrongSignatureLogger(), LoggerProtocol)
