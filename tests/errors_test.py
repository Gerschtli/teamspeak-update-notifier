from notifier import errors


def test_error() -> None:
    error = errors.Error()

    assert isinstance(error, Exception)
    assert error.exit_code == 127


def test_socket_connection_error() -> None:
    error = errors.SocketConnectionError()

    assert isinstance(error, Exception)
    assert isinstance(error, errors.Error)
    assert error.exit_code == 1


def test_message_error() -> None:
    error = errors.MessageError()

    assert isinstance(error, Exception)
    assert isinstance(error, errors.Error)
    assert error.exit_code == 2


def test_server_disconnect_error() -> None:
    error = errors.ServerDisconnectError()

    assert isinstance(error, Exception)
    assert isinstance(error, errors.Error)
    assert error.exit_code == 3


def test_sig_term_error() -> None:
    error = errors.SigTermError()

    assert isinstance(error, Exception)
    assert isinstance(error, errors.Error)
    assert error.exit_code == 4


def test_invalid_argument_error() -> None:
    error = errors.InvalidArgumentError()

    assert isinstance(error, Exception)
    assert isinstance(error, errors.Error)
    assert error.exit_code == 5


def test_config_error() -> None:
    error = errors.ConfigError()

    assert isinstance(error, Exception)
    assert isinstance(error, errors.Error)
    assert error.exit_code == 6
