from emptylog.call_data import LoggerCallData


def test_create_call_data_and_check_the_data():
    data = LoggerCallData('kek', (), {})

    assert data.message == 'kek'
    assert data.args == ()
    assert data.kwargs == {}
