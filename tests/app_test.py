import configparser
import logging
import unittest
from unittest.mock import patch, Mock, PropertyMock

from notifier import app


class AppTest(unittest.TestCase):
    @patch("configparser.ConfigParser", autospec=True)
    @patch("argparse.ArgumentParser", autospec=True)
    def test_config(self, mock_argparser: Mock, mock_configparser: Mock) -> None:
        namespace = Mock()
        type(namespace).config = PropertyMock(return_value="path/to/config")

        argparser = mock_argparser.return_value
        argparser.parse_args.return_value = namespace

        config = mock_configparser.return_value

        # pylint: disable=protected-access
        result = app._setup_config()

        mock_argparser.assert_called_once_with()
        argparser.add_argument.assert_called_once_with("config", help="Path to config file.")
        argparser.parse_args.assert_called_once_with()

        mock_configparser.assert_called_once_with()
        config.read.assert_called_once_with("path/to/config")

        self.assertEqual(config, result)

    @patch("logging.Logger", autospec=True)
    @patch("logging.StreamHandler", autospec=True)
    @patch("sys.stdout", autospec=True)
    @patch("logging.Formatter", autospec=True)
    def test_logger(self, mock_formatter: Mock, mock_stdout: Mock, mock_handler: Mock, mock_logger: Mock) -> None:
        formatter = mock_formatter.return_value
        handler = mock_handler.return_value
        logger = mock_logger.return_value

        # pylint: disable=protected-access
        result = app._setup_logger()

        mock_formatter.assert_called_once_with("[{levelname}] {message}", style="{")

        mock_handler.assert_called_once_with(mock_stdout)
        handler.setFormatter.assert_called_once_with(formatter)

        mock_logger.assert_called_once_with(name="notifier")
        logger.addHandler.assert_called_once_with(handler)

        self.assertEqual(logger, result)

    def test_constants(self) -> None:
        self.assertEqual(app.LOGGER_NAME, "notifier")
        self.assertIsInstance(app.CONFIG, configparser.ConfigParser)
        self.assertIsInstance(app.LOGGER, logging.Logger)