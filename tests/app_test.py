from unittest.mock import Mock, PropertyMock, patch

from notifier import app


@patch("configparser.ConfigParser", autospec=True)
@patch("argparse.ArgumentParser", autospec=True)
def test_build_config(mock_argparser: Mock, mock_configparser: Mock) -> None:
    namespace = Mock()
    type(namespace).config = PropertyMock(return_value="path/to/config")

    argparser = mock_argparser.return_value
    argparser.parse_args.return_value = namespace

    config = mock_configparser.return_value

    result = app.build_config()

    mock_argparser.assert_called_once_with()
    argparser.add_argument.assert_called_once_with("config", help="Path to config file.")
    argparser.parse_args.assert_called_once_with()

    mock_configparser.assert_called_once_with()
    config.read.assert_called_once_with("path/to/config")

    assert config == result
