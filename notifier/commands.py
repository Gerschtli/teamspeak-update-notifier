from abc import abstractmethod
from typing import Dict, Optional

from . import errors
from .message import Message


class Response:
    def __init__(self, result: str):
        self.result = result


class Command:
    def __init__(self,
                 command: str,
                 value_params: Optional[Dict[str, str]] = None) -> None:
        self.message = Message(command, value_params)

    def check_error(self, message: Message) -> None:
        if message.command == "error" and message.param("msg") == "ok":
            return

        raise errors.MessageError(f"error last command: {self.message}")


class QueryCommand(Command):
    @abstractmethod
    def handle(self, message: Message) -> Optional[Response]:
        raise NotImplementedError()


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

    def handle(self, message: Message) -> Optional[Response]:
        return None


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

    def handle(self, message: Message) -> Optional[Response]:
        return None


class Use(Command):
    def __init__(self, server_id: str) -> None:
        super().__init__(
            "use",
            {"sid": server_id},
        )


class Whoami(QueryCommand):
    def __init__(self) -> None:
        super().__init__("whoami")

    def handle(self, message: Message) -> Optional[Response]:
        client_id = message.param("client_id")

        if client_id is None:
            raise errors.MessageError("whoami failed")

        return Response(client_id)
