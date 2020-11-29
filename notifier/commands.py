from typing import Dict, NamedTuple, Optional, TypeVar

from . import errors
from .message import Message

T = TypeVar('T')


class Command:
    def __init__(self,
                 command: str,
                 value_params: Optional[Dict[str, str]] = None) -> None:
        self.message = Message(command, value_params)

    def check_error(self, message: Optional[Message]) -> None:
        if message is not None and message.command == "error" and message.param("msg") == "ok":
            return

        raise errors.MessageError(f"error last command: {self.message}")


class QueryCommand(Command):
    def __init__(self, command: str, value_params: Optional[Dict[str, str]] = None) -> None:
        super().__init__(command, value_params)

    def handle(self, message: Optional[Message]) -> T:
        return None


class Login(Command):
    def __init__(self, username: str, password: str) -> None:
        super().__init__(
            "login",
            {
                "client_login_name": username,
                "client_login_password": password,
            },
        )


class KeepAlive(QueryCommand):
    """
    Just any command which is executed regularly to keep connection alive.
    """

    def __init__(self) -> None:
        super().__init__("version")


class NotifyRegister(Command):
    def __init__(self) -> None:
        super().__init__(
            "servernotifyregister",
            {"event": "server"},
        )


class Quit(Command):
    def __init__(self) -> None:
        super().__init__("quit")


class SendMessage(QueryCommand):
    def __init__(self, client_id: str, message: str) -> None:
        super().__init__(
            "sendtextmessage",
            {
                "targetmode": "1",
                "target": client_id,
                "msg": message,
            },
        )


class Use(Command):
    def __init__(self, server_id: str) -> None:
        super().__init__(
            "use",
            {"sid": server_id},
        )


class WhoamiResponse(NamedTuple):
    client_id: str


class Whoami(QueryCommand):
    def __init__(self) -> None:
        super().__init__("whoami")

    def handle(self, message: Optional[Message]) -> T:
        client_id = message.param("client_id")

        if client_id is None:
            raise errors.MessageError("whoami failed")

        return WhoamiResponse(client_id)
