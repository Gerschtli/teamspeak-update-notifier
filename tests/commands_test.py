import configparser
import unittest
from unittest.mock import call, Mock

from notifier import app, commands


class CommandsTest(unittest.TestCase):
    def test_login(self) -> None:
        config = Mock(spec_set=configparser.ConfigParser)
        config.get.side_effect = ["username", "password"]
        app.CONFIG = config

        message = commands.Login()

        config.get.assert_has_calls([call("ts3", "username"), call("ts3", "password")])
        self.assertEqual(config.get.call_count, 2)

        self.assertIsInstance(message, commands.Login)
        self.assertEqual(message.command, "login")
        self.assertEqual(message.param("client_login_name"), "username")
        self.assertEqual(message.param("client_login_password"), "password")
        self.assertEqual(str(message), "login client_login_name=username client_login_password=password")

    def test_notify_register(self) -> None:
        message = commands.NotifyRegister()

        self.assertIsInstance(message, commands.NotifyRegister)
        self.assertEqual(message.command, "servernotifyregister")
        self.assertEqual(message.param("event"), "server")
        self.assertEqual(str(message), "servernotifyregister event=server")

    def test_quit(self) -> None:
        message = commands.Quit()

        self.assertIsInstance(message, commands.Quit)
        self.assertEqual(message.command, "quit")
        self.assertEqual(str(message), "quit")

    def test_send_message(self) -> None:
        message = commands.SendMessage("123", "text")

        self.assertIsInstance(message, commands.SendMessage)
        self.assertEqual(message.command, "sendtextmessage")
        self.assertEqual(message.param("targetmode"), "1")
        self.assertEqual(message.param("target"), "123")
        self.assertEqual(message.param("msg"), "text")
        self.assertEqual(str(message), "sendtextmessage targetmode=1 target=123 msg=text")

    def test_use(self) -> None:
        config = Mock(spec_set=configparser.ConfigParser)
        app.CONFIG = config
        config.get.return_value = "654"

        message = commands.Use()

        config.get.assert_called_with("ts3", "server_id")
        self.assertEqual(config.get.call_count, 1)

        self.assertIsInstance(message, commands.Use)
        self.assertEqual(message.command, "use")
        self.assertEqual(message.param("sid"), "654")
        self.assertEqual(str(message), "use sid=654")

    def test_whoami(self) -> None:
        message = commands.Whoami()

        self.assertIsInstance(message, commands.Whoami)
        self.assertEqual(message.command, "whoami")
        self.assertEqual(str(message), "whoami")
