from .message import Message


class Login(Message):
    def __init__(self, username: str, password: str) -> None:
        super().__init__(
            "login",
            {
                "client_login_name": username,
                "client_login_password": password,
            },
        )


class NotifyRegister(Message):
    def __init__(self) -> None:
        super().__init__(
            "servernotifyregister",
            {"event": "server"},
        )


class Quit(Message):
    def __init__(self) -> None:
        super().__init__("quit")


class SendMessage(Message):
    def __init__(self, client_id: str, message: str) -> None:
        super().__init__(
            "sendtextmessage",
            {
                "targetmode": "1",
                "target": client_id,
                "msg": message,
            },
        )


class Use(Message):
    def __init__(self, server_id: str) -> None:
        super().__init__(
            "use",
            {"sid": server_id},
        )


class Whoami(Message):
    def __init__(self) -> None:
        super().__init__("whoami")


class CommandFactory:
    def __init__(self, username: str, password: str, server_id: str) -> None:
        self.username = username
        self.password = password
        self.server_id = server_id

    def login(self) -> Login:
        return Login(self.username, self.password)

    @staticmethod
    def notify_register() -> NotifyRegister:
        return NotifyRegister()

    @staticmethod
    def quit() -> Quit:
        return Quit()

    @staticmethod
    def send_message(client_id: str, message: str) -> SendMessage:
        return SendMessage(client_id, message)

    def use(self) -> Use:
        return Use(self.server_id)

    @staticmethod
    def whoami() -> Whoami:
        return Whoami()
