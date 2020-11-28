from typing import Dict, Optional

from .message import Message


class Command(Message):
    def __init__(self,
                 command: str,
                 value_params: Optional[Dict[str, str]] = None,
                 has_response: bool = False) -> None:
        super().__init__(command, value_params)

        self.has_response = has_response


class Login(Command):
    def __init__(self, username: str, password: str) -> None:
        super().__init__(
            "login",
            {
                "client_login_name": username,
                "client_login_password": password,
            },
        )


class KeepAlive(Command):
    """
    Just any command which is executed regularly to keep connection alive.
    """

    def __init__(self) -> None:
        super().__init__("version", has_response=True)


class NotifyRegister(Command):
    def __init__(self) -> None:
        super().__init__(
            "servernotifyregister",
            {"event": "server"},
        )


class Quit(Command):
    def __init__(self) -> None:
        super().__init__("quit")


class SendMessage(Command):
    def __init__(self, client_id: str, message: str) -> None:
        super().__init__(
            "sendtextmessage",
            {
                "targetmode": "1",
                "target": client_id,
                "msg": message,
            },
            has_response=True,
        )


class Use(Command):
    def __init__(self, server_id: str) -> None:
        super().__init__(
            "use",
            {"sid": server_id},
        )


class Whoami(Command):
    def __init__(self) -> None:
        super().__init__("whoami", has_response=True)
