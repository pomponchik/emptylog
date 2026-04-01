import logging

from emptylog import EmptyLogger
from emptylog.abstract_logger import AbstractLogger


def test_search_callable_attributes():
    attribute_names = [
        'debug',
        'info',
        'warning',
        'error',
        'exception',
        'critical',
    ]

    empty_logger = EmptyLogger()
    real_logger = logging.getLogger('kek')

    for name in attribute_names:
        for logger in [empty_logger, real_logger]:
            method = getattr(logger, name)

            assert callable(method)

            method('kek')
            method('kek %s', 'lol')
            method('kek %s', 'lol', extra={'lol': 'kek'})


def test_repr_empty_logger():
    assert repr(EmptyLogger()) == 'EmptyLogger()'


def test_methods_return_none():
    logger = EmptyLogger()

    for name in ['debug', 'info', 'warning', 'error', 'exception', 'critical']:
        result = getattr(logger, name)('message', 'arg', key='value')

        assert result is None


def test_empty_logger_is_abstract_logger():
    assert isinstance(EmptyLogger(), AbstractLogger)
