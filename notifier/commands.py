from . import app, message


class Login(message.Message):
    def __init__(self) -> None:
        super().__init__(
            "login",
            {
                "client_login_name": app.CONFIG.get("ts3", "username"),
                "client_login_password": app.CONFIG.get("ts3", "password"),
            },
        )


class NotifyRegister(message.Message):
    def __init__(self) -> None:
        super().__init__(
            "servernotifyregister",
            {"event": "server"},
        )


class Quit(message.Message):
    def __init__(self) -> None:
        super().__init__("quit")


class SendMessage(message.Message):
    def __init__(self, client_id: str, message: str) -> None:
        super().__init__(
            "sendtextmessage",
            {
                "targetmode": "1",
                "target": client_id,
                "msg": message,
            },
        )


class Use(message.Message):
    def __init__(self) -> None:
        super().__init__(
            "use",
            {"sid": app.CONFIG.get("ts3", "server_id")},
        )


class Whoami(message.Message):
    def __init__(self) -> None:
        super().__init__("whoami")
