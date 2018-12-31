import configparser
import logging
import signal
import sys
from typing import Any
from unittest.mock import Mock, patch

from notifier import errors, main


@patch("notifier.app.start")
@patch("signal.signal")
@patch("notifier.app.build_config")
@patch("logging.basicConfig")
def test_main(
        mock_basic_config: Mock,
        mock_build_config: Mock,
        mock_signal: Mock,
        mock_start: Mock,
) -> None:
    config = Mock(spec_set=configparser.ConfigParser)
    mock_build_config.return_value = config

    main.main()

    mock_basic_config.assert_called_once_with(
        level=logging.DEBUG,
        stream=sys.stdout,
    )
    mock_build_config.assert_called_once_with()
    mock_signal.assert_called_once_with(signal.SIGTERM, main._sigterm_handler)
    mock_start.assert_called_once_with(config)


@patch("sys.exit")
@patch("notifier.app.start")
@patch("signal.signal")
@patch("notifier.app.build_config")
@patch("logging.basicConfig")
def test_main_when_keyboard_interrupt(  # type: ignore
        mock_basic_config: Mock,
        mock_build_config: Mock,
        mock_signal: Mock,
        mock_start: Mock,
        mock_exit: Mock,
        caplog: Any,  # _pytest.logging.LogCaptureFixture
) -> None:
    config = Mock(spec_set=configparser.ConfigParser)
    mock_build_config.return_value = config

    mock_start.side_effect = KeyboardInterrupt()

    main.main()

    mock_basic_config.assert_called_once_with(
        level=logging.DEBUG,
        stream=sys.stdout,
    )
    mock_build_config.assert_called_once_with()
    mock_signal.assert_called_once_with(signal.SIGTERM, main._sigterm_handler)
    mock_start.assert_called_once_with(config)
    mock_exit.assert_called_once_with(errors.SigTermError.exit_code)

    assert caplog.record_tuples == [
        ("notifier.main", logging.ERROR, "exception occured in main, stopping application"),
    ]


@patch("sys.exit")
@patch("notifier.app.start")
@patch("signal.signal")
@patch("notifier.app.build_config")
@patch("logging.basicConfig")
def test_main_when_error(  # type: ignore
        mock_basic_config: Mock,
        mock_build_config: Mock,
        mock_signal: Mock,
        mock_start: Mock,
        mock_exit: Mock,
        caplog: Any,  # _pytest.logging.LogCaptureFixture
) -> None:
    config = Mock(spec_set=configparser.ConfigParser)
    mock_build_config.return_value = config

    mock_start.side_effect = errors.MessageError("message")

    main.main()

    mock_basic_config.assert_called_once_with(
        level=logging.DEBUG,
        stream=sys.stdout,
    )
    mock_build_config.assert_called_once_with()
    mock_signal.assert_called_once_with(signal.SIGTERM, main._sigterm_handler)
    mock_start.assert_called_once_with(config)
    mock_exit.assert_called_once_with(errors.MessageError.exit_code)

    assert caplog.record_tuples == [
        ("notifier.main", logging.ERROR, "exception occured in main, stopping application"),
    ]


@patch("sys.exit")
@patch("notifier.app.start")
@patch("signal.signal")
@patch("notifier.app.build_config")
@patch("logging.basicConfig")
def test_main_when_other_exception(  # type: ignore
        mock_basic_config: Mock,
        mock_build_config: Mock,
        mock_signal: Mock,
        mock_start: Mock,
        mock_exit: Mock,
        caplog: Any,  # _pytest.logging.LogCaptureFixture
) -> None:
    config = Mock(spec_set=configparser.ConfigParser)
    mock_build_config.return_value = config

    expected_exception = Exception("message")
    mock_start.side_effect = expected_exception

    exception = None
    try:
        main.main()
    except Exception as ex:
        exception = ex

    mock_basic_config.assert_called_once_with(
        level=logging.DEBUG,
        stream=sys.stdout,
    )
    mock_build_config.assert_called_once_with()
    mock_signal.assert_called_once_with(signal.SIGTERM, main._sigterm_handler)
    mock_start.assert_called_once_with(config)

    assert mock_exit.call_count == 0

    assert caplog.record_tuples == []

    assert exception == expected_exception


def test_sigterm_handler() -> None:
    exception = None
    try:
        main._sigterm_handler(Mock(), Mock())
    except Exception as ex:
        exception = ex

    assert isinstance(exception, errors.SigTermError)
    assert str(exception) == "process killed via SIGTERM"
