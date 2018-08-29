import unittest

from notifier.message import Message


class MessageTest(unittest.TestCase):
    def test_build_from_string(self):
        message = Message.build_from_string("login user=hans password=georg")
        self.assertEqual(message.command, "login")
        self.assertEqual(message.param("user"), "hans")
        self.assertEqual(message.param("password"), "georg")

        string_repr = str(message)
        self.assertTrue(string_repr.startswith("login "))
        self.assertIn("user=hans", string_repr)
        self.assertIn("password=georg", string_repr)
