import unittest

from notifier.message import Message


class MessageTest(unittest.TestCase):
    def test_build_from_string(self):
        message = Message.build_from_string("login user=hans password=georg")
        self.assertEqual(message.command, "login")
        self.assertEqual(message.param("user"), "hans")
        self.assertEqual(message.param("password"), "georg")

        repr = str(message)
        self.assertTrue(repr.startswith("login "))
        self.assertIn("user=hans", repr)
        self.assertIn("password=georg", repr)
