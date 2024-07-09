import logging

from emptylog import LoggerProtocol, EmptyLogger, LoggersGroup, MemoryLogger, PrintingLogger


def test_positive_examples_of_runtime_check():
    assert isinstance(logging, LoggerProtocol)
    assert isinstance(logging.getLogger('kek'), LoggerProtocol)
    assert isinstance(logging.getLogger('kek'), LoggerProtocol)
    assert isinstance(EmptyLogger(), LoggerProtocol)
    assert isinstance(LoggersGroup(), LoggerProtocol)
    assert isinstance(MemoryLogger(), LoggerProtocol)
    assert isinstance(PrintingLogger(), LoggerProtocol)


def test_negative_examples_of_runtime_check():
    assert not isinstance(1, LoggerProtocol)
    assert not isinstance('logging', LoggerProtocol)
