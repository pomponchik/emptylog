import io
import re
from contextlib import redirect_stdout

import pytest

from emptylog import PrintingLogger, LoggerProtocol


def test_printing_logger_is_logger():
    assert isinstance(PrintingLogger(), LoggerProtocol)


@pytest.mark.parametrize(
    ['method', 'result_tail'],
    (
        (PrintingLogger().debug, ' | DEBUG     | kek'),
        (PrintingLogger().info, ' | INFO      | kek'),
        (PrintingLogger().warning, ' | WARNING   | kek'),
        (PrintingLogger().error, ' | ERROR     | kek'),
        (PrintingLogger().exception, ' | EXCEPTION | kek'),
        (PrintingLogger().critical, ' | CRITICAL  | kek'),

        (PrintingLogger(separator='*').debug, ' * DEBUG     * kek'),
        (PrintingLogger(separator='*').info, ' * INFO      * kek'),
        (PrintingLogger(separator='*').warning, ' * WARNING   * kek'),
        (PrintingLogger(separator='*').error, ' * ERROR     * kek'),
        (PrintingLogger(separator='*').exception, ' * EXCEPTION * kek'),
        (PrintingLogger(separator='*').critical, ' * CRITICAL  * kek'),
    ),
)
def test_check_simple_output(method, result_tail):
    remove_suffix = lambda input_string, suffix: input_string[:-len(suffix)] if suffix and input_string.endswith(suffix) else input_string

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        method('kek')

    printed = buffer.getvalue()

    assert printed.endswith(result_tail + '\n')

    time_stamp = remove_suffix(printed, result_tail + '\n') # expected format: 2024-07-08 19:09:48.226667

    assert len(time_stamp.split()) == 2

    date = time_stamp.split()[0]
    time = time_stamp.split()[1]

    assert re.match(r'[\d]{4}-[\d]{2}-[\d]{2}', date) is not None

    time_before_dot = time.split('.')[0]
    time_after_dot = time.split('.')[1]

    assert len(time.split('.')) == 2
    assert re.match(r'[\d]{2}:[\d]{2}:[\d]{2}', time_before_dot) is not None
    assert time_after_dot.isdigit()
