import logging

import pytest
import full_match
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
    ['wrong_logger', 'exception_message'],
    (
        (1, 'A logger group can only be created from loggers. You passed 1 (int).'),
        ('kek', 'A logger group can only be created from loggers. You passed \'kek\' (str).'),
        (None, 'A logger group can only be created from loggers. You passed None (NoneType).'),
    ),
)
def test_create_group_with_not_loggers(wrong_logger, exception_message):
    with pytest.raises(TypeError, match=full_match(exception_message)):
        LoggersGroup(wrong_logger)


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
    assert len(another_logger + LoggersGroup()) == 1
    assert (another_logger + LoggersGroup()).loggers[0] is another_logger


@pytest.mark.parametrize(
    ['third_party_logger'],
    (
        (loguru_logger,),
        (logging,),
        (logging.getLogger('kek'),),
    ),
)
def test_empty_group_plus_third_party_logger(third_party_logger):
    first_group = LoggersGroup()

    sum = first_group + third_party_logger

    assert type(sum) is LoggersGroup
    assert sum is not first_group
    assert len(sum.loggers) == 1
    assert len(sum) == 1
    assert sum.loggers[0] is third_party_logger


@pytest.mark.parametrize(
    ['third_party_logger'],
    (
        (loguru_logger,),
        (logging,),
        (logging.getLogger('kek'),),
    ),
)
def test_third_party_logger_plus_empty_group(third_party_logger):
    first_group = LoggersGroup()

    sum = third_party_logger + first_group

    assert type(sum) is LoggersGroup
    assert sum is not first_group
    assert len(sum.loggers) == 1
    assert len(sum) == 1
    assert sum.loggers[0] is third_party_logger


@pytest.mark.parametrize(
    ['loggers'],
    (
        ([loguru_logger, logging, logging.getLogger('kek')],),
        ([MemoryLogger(), MemoryLogger()],),
        ([MemoryLogger()],),
        ([],),
    ),
)
def test_iteration_by_group(loggers):
    group = LoggersGroup(*loggers)

    assert loggers == [x for x in group]
