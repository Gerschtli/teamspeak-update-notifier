import unittest

from notifier.errors import Error, SocketConnectionError, MessageError, \
    ServerDisconnectError, SigTermError, EmptyMessageError


class ErrorsTest(unittest.TestCase):
    def test_error(self) -> None:
        error = Error()

        self.assertIsInstance(error, Exception)
        self.assertEqual(error.exit_code, 127)

    def test_socket_connection_error(self) -> None:
        error = SocketConnectionError()

        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, Error)
        self.assertEqual(error.exit_code, 1)

    def test_message_error(self) -> None:
        error = MessageError()

        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, Error)
        self.assertEqual(error.exit_code, 2)

    def test_server_disconnect_error(self) -> None:
        error = ServerDisconnectError()

        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, Error)
        self.assertEqual(error.exit_code, 3)

    def test_sig_term_error(self) -> None:
        error = SigTermError()

        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, Error)
        self.assertEqual(error.exit_code, 4)

    def test_empty_message_error(self) -> None:
        error = EmptyMessageError()

        self.assertIsInstance(error, Exception)
        self.assertIsInstance(error, Error)
        self.assertEqual(error.exit_code, 5)
