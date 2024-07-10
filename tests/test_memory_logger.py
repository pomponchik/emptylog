from emptylog import MemoryLogger, LoggerProtocol
from emptylog.memory_logger import LoggerCallData


def test_memory_logger_is_logger():
    assert isinstance(MemoryLogger(), LoggerProtocol)


def test_memory_logger_is_working():
    attribute_names = [
        'debug',
        'info',
        'warning',
        'error',
        'exception',
        'critical',
    ]

    logger = MemoryLogger()

    for name in attribute_names:
        method = getattr(logger, name)

        assert callable(method)

        for number in range(3):
            method(f'kek_{name}', 'lol', 'cheburek', name, pek='mek', kekokek=name)

    assert len(logger.data.debug) == 3
    assert len(logger.data.info) == 3
    assert len(logger.data.warning) == 3
    assert len(logger.data.error) == 3
    assert len(logger.data.exception) == 3
    assert len(logger.data.critical) == 3

    assert logger.data.debug[0] == logger.data.debug[1] == logger.data.debug[2]
    assert logger.data.info[0] == logger.data.info[1] == logger.data.info[2]
    assert logger.data.warning[0] == logger.data.warning[1] == logger.data.warning[2]
    assert logger.data.error[0] == logger.data.error[1] == logger.data.error[2]
    assert logger.data.exception[0] == logger.data.exception[1] == logger.data.exception[2]
    assert logger.data.critical[0] == logger.data.critical[1] == logger.data.critical[2]

    assert logger.data.debug[0] == LoggerCallData(message='kek_debug', args=('lol', 'cheburek', 'debug'), kwargs={'pek': 'mek', 'kekokek': 'debug'})
    assert logger.data.info[0] == LoggerCallData(message='kek_info', args=('lol', 'cheburek', 'info'), kwargs={'pek': 'mek', 'kekokek': 'info'})
    assert logger.data.warning[0] == LoggerCallData(message='kek_warning', args=('lol', 'cheburek', 'warning'), kwargs={'pek': 'mek', 'kekokek': 'warning'})
    assert logger.data.error[0] == LoggerCallData(message='kek_error', args=('lol', 'cheburek', 'error'), kwargs={'pek': 'mek', 'kekokek': 'error'})
    assert logger.data.exception[0] == LoggerCallData(message='kek_exception', args=('lol', 'cheburek', 'exception'), kwargs={'pek': 'mek', 'kekokek': 'exception'})
    assert logger.data.critical[0] == LoggerCallData(message='kek_critical', args=('lol', 'cheburek', 'critical'), kwargs={'pek': 'mek', 'kekokek': 'critical'})


def test_repr_memory_logger():
    assert repr(MemoryLogger()) == 'MemoryLogger()'
