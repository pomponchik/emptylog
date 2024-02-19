from emptylog.call_data import LoggerCallData
from emptylog.accumulated_data import LoggerAccumulatedData


def test_fill_accumulated_data_and_check_size():
    data = LoggerAccumulatedData()

    lists = [
        data.debug,
        data.info,
        data.warning,
        data.error,
        data.exception,
        data.critical,
    ]

    logs_sum = 0

    for index, logs_list in enumerate(lists):
        assert len(data) == logs_sum

        for _ in range(index + 1):
            logs_list.append(LoggerCallData('some message', (), {}))
            logs_sum += 1

            assert len(data) == logs_sum

    assert len(data) == 21
