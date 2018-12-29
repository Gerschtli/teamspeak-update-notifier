import unittest

from notifier import errors


class ErrorsTest(unittest.TestCase):
    def test_error(self) -> None:
        error = errors.Error()

        self.assertIsInstance(error, Exception)
        self.assertEqual(error.exit_code, 127)

    def test_socket_connection_error(self) -> None:
        error = errors.SocketConnectionError()

        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, errors.Error)
        self.assertEqual(error.exit_code, 1)

    def test_message_error(self) -> None:
        error = errors.MessageError()

        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, errors.Error)
        self.assertEqual(error.exit_code, 2)

    def test_server_disconnect_error(self) -> None:
        error = errors.ServerDisconnectError()

        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, errors.Error)
        self.assertEqual(error.exit_code, 3)

    def test_sig_term_error(self) -> None:
        error = errors.SigTermError()

        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, errors.Error)
        self.assertEqual(error.exit_code, 4)

    def test_empty_message_error(self) -> None:
        error = errors.EmptyMessageError()

        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, errors.Error)
        self.assertEqual(error.exit_code, 5)
