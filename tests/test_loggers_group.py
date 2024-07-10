from emptylog import LoggersGroup, MemoryLogger

import pytest


@pytest.mark.parametrize(
    ['get_method'],
    (
        (lambda x: x.debug,),
        (lambda x: x.info,),
        (lambda x: x.warning,),
        (lambda x: x.error,),
        (lambda x: x.exception,),
        (lambda x: x.critical,),
    ),
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
    assert (another_logger + LoggersGroup()).loggers[0] is another_logger
