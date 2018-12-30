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
