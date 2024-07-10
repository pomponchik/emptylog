import logging

import pytest
import full_match
from loguru import logger as loguru_logger

from emptylog.abstract_logger import AbstractLogger
from emptylog import EmptyLogger, LoggersGroup, MemoryLogger, PrintingLogger


@pytest.mark.parametrize(
    ['first_logger'],
    (
        (EmptyLogger(),),
        (MemoryLogger(),),
        (PrintingLogger(),),
    ),
)
@pytest.mark.parametrize(
    ['second_logger'],
    (
        (EmptyLogger(),),
        (MemoryLogger(),),
        (PrintingLogger(),),
        (logging,),
        (logging.getLogger('kek'),),
        (loguru_logger,),
    ),
)
def test_sum_of_inner_loggers(first_logger, second_logger):
    sum = first_logger + second_logger

    assert isinstance(sum, LoggersGroup)

    assert sum is not first_logger
    assert sum is not second_logger

    assert sum.loggers[0] is first_logger
    assert sum.loggers[1] is second_logger


@pytest.mark.parametrize(
    ['first_logger'],
    (
        (logging,),
        (logging.getLogger('kek'),),
        (loguru_logger,),
    ),
)
@pytest.mark.parametrize(
    ['second_logger'],
    (
        (EmptyLogger(),),
        (MemoryLogger(),),
        (PrintingLogger(),),
    ),
)
def test_sum_with_another_loggers_as_first_operand(first_logger, second_logger):
    sum = first_logger + second_logger

    assert isinstance(sum, LoggersGroup)

    assert sum is not first_logger
    assert sum is not second_logger

    assert sum.loggers[0] is first_logger
    assert sum.loggers[1] is second_logger


@pytest.mark.parametrize(
    ['logger'],
    (
        (EmptyLogger(),),
        (LoggersGroup(),),
        (MemoryLogger(),),
        (PrintingLogger(),),
    ),
)
def test_all_loggers_are_instances_of_abstract_logger(logger):
    assert isinstance(logger, AbstractLogger)


@pytest.mark.parametrize(
    ['logger'],
    (
        (EmptyLogger(),),
        (LoggersGroup(),),
        (MemoryLogger(),),
        (PrintingLogger(),),
    ),
)
@pytest.mark.parametrize(
    ['wrong_operand'],
    (
        (1,),
        ('kek',),
        (None,),
    ),
)
def test_sum_with_wrong_first_operand(logger, wrong_operand):
    with pytest.raises(NotImplementedError, match=full_match('The addition operation is defined only for loggers.')):
        wrong_operand + logger


@pytest.mark.parametrize(
    ['logger'],
    (
        (EmptyLogger(),),
        (LoggersGroup(),),
        (MemoryLogger(),),
        (PrintingLogger(),),
    ),
)
@pytest.mark.parametrize(
    ['wrong_operand'],
    (
        (1,),
        ('kek',),
        (None,),
    ),
)
def test_sum_with_wrong_second_operand(logger, wrong_operand):
    with pytest.raises(NotImplementedError, match=full_match('The addition operation is defined only for loggers.')):
        logger + wrong_operand


def test_sum_of_three_loggers():
    first_logger = EmptyLogger()
    second_logger = MemoryLogger()
    third_logger = PrintingLogger()

    sum = first_logger + second_logger + third_logger

    assert isinstance(sum, LoggersGroup)

    assert len(sum) == 3
    assert len(sum.loggers) == 3

    assert sum.loggers[0] is first_logger
    assert sum.loggers[1] is second_logger
    assert sum.loggers[2] is third_logger
