from unittest.mock import Mock, patch


@patch("notifier.main.main")
def test_main(mock_main: Mock) -> None:
    from notifier import __main__

    assert __main__  # silence pyflakes

    mock_main.assert_called_once_with()
