import logging

from loguru import logger as loguru_logger

from emptylog import LoggerProtocol, EmptyLogger, LoggersGroup, MemoryLogger, PrintingLogger


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
