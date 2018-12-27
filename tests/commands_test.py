import unittest

from notifier.commands import CommandFactory, Login, NotifyRegister, Quit, \
    SendMessage, Use, Whoami


class CommandFactoryTest(unittest.TestCase):
    def test_login(self):
        factory = CommandFactory("username", "password", None)
        message = factory.login()

        self.assertIsInstance(message, Login)
        self.assertEqual(message.command(), "login")
        self.assertEqual(message.param("client_login_name"), "username")
        self.assertEqual(message.param("client_login_password"), "password")
        self.assertEqual(
            str(message),
            "login client_login_name=username client_login_password=password")

    def test_notify_register(self):
        factory = CommandFactory(None, None, None)
        message = factory.notify_register()

        self.assertIsInstance(message, NotifyRegister)
        self.assertEqual(message.command(), "servernotifyregister")
        self.assertEqual(message.param("event"), "server")
        self.assertEqual(str(message), "servernotifyregister event=server")

    def test_quit(self):
        factory = CommandFactory(None, None, None)
        message = factory.quit()

        self.assertIsInstance(message, Quit)
        self.assertEqual(message.command(), "quit")
        self.assertEqual(str(message), "quit")

    def test_send_message(self):
        factory = CommandFactory(None, None, None)
        message = factory.send_message("123", "text")

        self.assertIsInstance(message, SendMessage)
        self.assertEqual(message.command(), "sendtextmessage")
        self.assertEqual(message.param("targetmode"), "1")
        self.assertEqual(message.param("target"), "123")
        self.assertEqual(message.param("msg"), "text")
        self.assertEqual(
            str(message), "sendtextmessage targetmode=1 target=123 msg=text")

    def test_use(self):
        factory = CommandFactory(None, None, "654")
        message = factory.use()

        self.assertIsInstance(message, Use)
        self.assertEqual(message.command(), "use")
        self.assertEqual(message.param("sid"), "654")
        self.assertEqual(str(message), "use sid=654")

    def test_whoami(self):
        factory = CommandFactory(None, None, "654")
        message = factory.whoami()

        self.assertIsInstance(message, Whoami)
        self.assertEqual(message.command(), "whoami")
        self.assertEqual(str(message), "whoami")
