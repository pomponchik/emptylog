import logging

import pytest
from full_match import match
from loguru import logger as loguru_logger

from emptylog import LoggersGroup, MemoryLogger


def test_len_of_group():
    assert len(LoggersGroup()) == 0
    assert len(LoggersGroup(MemoryLogger())) == 1
    assert len(LoggersGroup(MemoryLogger(), MemoryLogger())) == 2
    assert len(LoggersGroup(MemoryLogger(), MemoryLogger(), MemoryLogger())) == 3
    assert len(LoggersGroup(MemoryLogger(), MemoryLogger(), MemoryLogger(), MemoryLogger())) == 4

    assert len(LoggersGroup() + LoggersGroup()) == 0
    assert len(LoggersGroup() + MemoryLogger()) == 1
    assert len(MemoryLogger() + MemoryLogger()) == 2
    assert len(MemoryLogger() + MemoryLogger() + MemoryLogger()) == 3


@pytest.mark.parametrize(
    ('wrong_logger', 'exception_message'),
    [
        (1, 'A logger group can only be created from loggers. You passed 1 (int).'),
        ('kek', 'A logger group can only be created from loggers. You passed \'kek\' (str).'),
        (None, 'A logger group can only be created from loggers. You passed None (NoneType).'),
    ],
)
def test_create_group_with_not_loggers(wrong_logger, exception_message):
    with pytest.raises(TypeError, match=match(exception_message)):
        LoggersGroup(wrong_logger)


@pytest.mark.parametrize(
    'get_method',
    [
        lambda x: x.debug,
        lambda x: x.info,
        lambda x: x.warning,
        lambda x: x.error,
        lambda x: x.exception,
        lambda x: x.critical,
    ],
)
def test_run_group_of_memory_loggers(get_method):
    first_internal_logger = MemoryLogger()
    second_internal_logger = MemoryLogger()
    group = LoggersGroup(first_internal_logger, second_internal_logger)

    get_method(group)('lol', 'kek', cheburek='pek')

    for internal_logger in first_internal_logger, second_internal_logger:
        assert len(get_method(internal_logger.data)) == 1
        assert get_method(internal_logger.data)[0].message == 'lol'
        assert get_method(internal_logger.data)[0].args == ('kek',)
        assert get_method(internal_logger.data)[0].kwargs == {'cheburek': 'pek'}


def test_repr_loggers_group():
    assert repr(LoggersGroup()) == 'LoggersGroup()'
    assert repr(LoggersGroup(LoggersGroup())) == 'LoggersGroup(LoggersGroup())'
    assert repr(LoggersGroup(MemoryLogger())) == 'LoggersGroup(MemoryLogger())'
    assert repr(LoggersGroup(MemoryLogger(), MemoryLogger())) == 'LoggersGroup(MemoryLogger(), MemoryLogger())'
    assert repr(LoggersGroup(MemoryLogger(), MemoryLogger(), MemoryLogger())) == 'LoggersGroup(MemoryLogger(), MemoryLogger(), MemoryLogger())'


def test_empty_group_plus_empty_group():
    assert type(LoggersGroup() + LoggersGroup()) is LoggersGroup
    assert (LoggersGroup() + LoggersGroup()).loggers == ()


def test_not_empty_group_plus_empty_group():
    first_internal_logger = MemoryLogger()
    second_internal_logger = MemoryLogger()

    assert type(LoggersGroup(first_internal_logger) + LoggersGroup()) is LoggersGroup
    assert type(LoggersGroup(first_internal_logger, second_internal_logger) + LoggersGroup()) is LoggersGroup

    assert len((LoggersGroup(first_internal_logger) + LoggersGroup()).loggers) == 1
    assert len((LoggersGroup(first_internal_logger, second_internal_logger) + LoggersGroup()).loggers) == 2

    assert (LoggersGroup(first_internal_logger) + LoggersGroup()).loggers[0] is first_internal_logger
    assert (LoggersGroup(first_internal_logger, second_internal_logger) + LoggersGroup()).loggers[0] is first_internal_logger
    assert (LoggersGroup(first_internal_logger, second_internal_logger) + LoggersGroup()).loggers[1] is second_internal_logger


def test_empty_group_plus_not_empty_group():
    first_internal_logger = MemoryLogger()
    second_internal_logger = MemoryLogger()

    assert type(LoggersGroup() + LoggersGroup(first_internal_logger)) is LoggersGroup
    assert type(LoggersGroup() + LoggersGroup(first_internal_logger, second_internal_logger)) is LoggersGroup

    assert len((LoggersGroup() + LoggersGroup(first_internal_logger)).loggers) == 1
    assert len((LoggersGroup() + LoggersGroup(first_internal_logger, second_internal_logger)).loggers) == 2

    assert (LoggersGroup() + LoggersGroup(first_internal_logger)).loggers[0] is first_internal_logger
    assert (LoggersGroup() + LoggersGroup(first_internal_logger, second_internal_logger)).loggers[0] is first_internal_logger
    assert (LoggersGroup() + LoggersGroup(first_internal_logger, second_internal_logger)).loggers[1] is second_internal_logger


def test_empty_group_plus_another_logger():
    another_logger = MemoryLogger()

    assert type(LoggersGroup() + another_logger) is LoggersGroup
    assert len((LoggersGroup() + another_logger).loggers) == 1
    assert (LoggersGroup() + another_logger).loggers[0] is another_logger


def test_another_logger_plus_empty_group():
    another_logger = MemoryLogger()

    assert type(another_logger + LoggersGroup()) is LoggersGroup
    assert len((another_logger + LoggersGroup()).loggers) == 1
    assert len(another_logger + LoggersGroup()) == 1
    assert (another_logger + LoggersGroup()).loggers[0] is another_logger


@pytest.mark.parametrize(
    'third_party_logger',
    [
        loguru_logger,
        logging,
        logging.getLogger('kek'),
    ],
)
def test_empty_group_plus_third_party_logger(third_party_logger):
    first_group = LoggersGroup()

    result = first_group + third_party_logger

    assert type(result) is LoggersGroup
    assert result is not first_group
    assert len(result.loggers) == 1
    assert len(result) == 1
    assert result.loggers[0] is third_party_logger


@pytest.mark.parametrize(
    'third_party_logger',
    [
        loguru_logger,
        logging,
        logging.getLogger('kek'),
    ],
)
def test_third_party_logger_plus_empty_group(third_party_logger):
    first_group = LoggersGroup()

    result = third_party_logger + first_group

    assert type(result) is LoggersGroup
    assert result is not first_group
    assert len(result.loggers) == 1
    assert len(result) == 1
    assert result.loggers[0] is third_party_logger


@pytest.mark.parametrize(
    'loggers',
    [
        [loguru_logger, logging, logging.getLogger('kek')],
        [MemoryLogger(), MemoryLogger()],
        [MemoryLogger()],
        [],
    ],
)
def test_iteration_by_group(loggers):
    group = LoggersGroup(*loggers)

    assert loggers == [x for x in group]


def test_calling_methods_on_empty_group_does_not_raise():
    group = LoggersGroup()

    group.debug('msg')
    group.info('msg')
    group.warning('msg')
    group.error('msg')
    group.exception('msg')
    group.critical('msg')


def test_loggers_are_called_in_order():
    call_order = []

    class RecordingLogger:
        def __init__(self, name):
            self.name = name
        def debug(self, *args, **kwargs): call_order.append(self.name)  # noqa: ARG002
        def info(self, *args, **kwargs): call_order.append(self.name)  # noqa: ARG002
        def warning(self, *args, **kwargs): call_order.append(self.name)  # noqa: ARG002
        def error(self, *args, **kwargs): call_order.append(self.name)  # noqa: ARG002
        def exception(self, *args, **kwargs): call_order.append(self.name)  # noqa: ARG002
        def critical(self, *args, **kwargs): call_order.append(self.name)  # noqa: ARG002

    first = RecordingLogger('first')
    second = RecordingLogger('second')
    third = RecordingLogger('third')
    group = LoggersGroup(first, second, third)

    group.debug('msg')

    assert call_order == ['first', 'second', 'third']


def test_run_single_logger_group():
    logger = MemoryLogger()
    group = LoggersGroup(logger)
    group.info('hello', 'arg', key='val')
    assert logger.data.info[0].message == 'hello'
    assert logger.data.info[0].args == ('arg',)
    assert logger.data.info[0].kwargs == {'key': 'val'}


def test_run_three_logger_group():
    loggers = [MemoryLogger(), MemoryLogger(), MemoryLogger()]
    group = LoggersGroup(*loggers)
    group.error('msg', 'arg', k='v')
    for logger in loggers:
        assert logger.data.error[0].message == 'msg'
        assert logger.data.error[0].args == ('arg',)
        assert logger.data.error[0].kwargs == {'k': 'v'}


def test_two_non_empty_groups_addition():
    logger1 = MemoryLogger()
    logger2 = MemoryLogger()
    logger3 = MemoryLogger()
    logger4 = MemoryLogger()

    result = LoggersGroup(logger1, logger2) + LoggersGroup(logger3, logger4)

    assert type(result) is LoggersGroup
    assert len(result) == 4
    assert result.loggers[0] is logger1
    assert result.loggers[1] is logger2
    assert result.loggers[2] is logger3
    assert result.loggers[3] is logger4
