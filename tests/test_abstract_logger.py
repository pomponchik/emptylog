import pytest

from emptylog.abstract_logger import AbstractLogger
from emptylog import EmptyLogger, LoggersGroup, MemoryLogger, PrintingLogger


@pytest.mark.parametrize(
    ['first_logger'],
    (
        (EmptyLogger(),),
        (LoggersGroup(),),
        (MemoryLogger(),),
        (PrintingLogger(),),
    ),
)
@pytest.mark.parametrize(
    ['second_logger'],
    (
        (EmptyLogger(),),
        (LoggersGroup(),),
        (MemoryLogger(),),
        (PrintingLogger(),),
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
