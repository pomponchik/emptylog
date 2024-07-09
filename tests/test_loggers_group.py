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
