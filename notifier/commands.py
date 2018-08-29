from .message import Message


class CommandFactory:
    def __init__(self, username, password, server_id):
        self.username = username
        self.password = password
        self.server_id = server_id

    def login(self):
        return Login(self.username, self.password)

    @staticmethod
    def notify_register():
        return NotifyRegister()

    @staticmethod
    def quit():
        return Quit()

    @staticmethod
    def send_message(client_id, message):
        return SendMessage(client_id, message)

    def use(self):
        return Use(self.server_id)

    @staticmethod
    def whoami():
        return Whoami()


class Login(Message):
    def __init__(self, username, password):
        super().__init__(
            "login",
            {
                "client_login_name": username,
                "client_login_password": password,
            },
        )


class NotifyRegister(Message):
    def __init__(self, ):
        super().__init__(
            "servernotifyregister",
            {"event": "server"},
        )


class Quit(Message):
    def __init__(self):
        super().__init__("quit")


class SendMessage(Message):
    def __init__(self, client_id, message):
        super().__init__(
            "sendtextmessage",
            {
                "targetmode": "1",
                "target": client_id,
                "msg": message,
            },
        )


class Use(Message):
    def __init__(self, server_id):
        super().__init__(
            "use",
            {"sid": server_id},
        )


class Whoami(Message):
    def __init__(self):
        super().__init__("whoami")
