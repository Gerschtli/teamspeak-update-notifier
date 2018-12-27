import unittest

from notifier.errors import EmptyMessageError
from notifier.message import Message


class MessageTest(unittest.TestCase):
    def test_build_from_string(self):
        message = Message.build_from_string(
            "login hello user=hans password=georg")
        self.assertEqual(message.command(), "login")
        self.assertEqual(message.param("user"), "hans")
        self.assertEqual(message.param("password"), "georg")

        string_repr = str(message)
        self.assertTrue(string_repr.startswith("login hello "))
        self.assertIn("user=hans", string_repr)
        self.assertIn("password=georg", string_repr)

    def test_build_from_string_with_special_chars(self):
        message = Message.build_from_string(r"command payload=test\sx\\o\/x\p")
        self.assertEqual(message.command(), "command")
        self.assertEqual(message.param("payload"), r"test x\o/x|")

        string_repr = str(message)
        self.assertEqual(string_repr, r"command payload=test\sx\\o\/x\p")

    def test_build_from_string_with_empty_message(self):
        exception = None

        try:
            Message.build_from_string("")
        except EmptyMessageError as ex:
            exception = ex

        self.assertEqual(str(exception), "empty message received")

    def test_init(self):
        message = Message("login", {
            "user": "hans",
            "password": "georg"
        }, ["hello"])
        self.assertEqual(message.command(), "login")
        self.assertEqual(message.param("user"), "hans")
        self.assertEqual(message.param("password"), "georg")

        string_repr = str(message)
        self.assertTrue(string_repr.startswith("login hello "))
        self.assertIn("user=hans", string_repr)
        self.assertIn("password=georg", string_repr)

    def test_init_with_special_chars(self):
        message = Message("command", {"payload": r"test x\o/x|"})
        self.assertEqual(message.command(), "command")
        self.assertEqual(message.param("payload"), r"test x\o/x|")

        string_repr = str(message)
        self.assertEqual(string_repr, r"command payload=test\sx\\o\/x\p")
