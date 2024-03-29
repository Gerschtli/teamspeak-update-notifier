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


class ConsumerCommand(Command):
    pass


class QueryCommand(Command):
    @abstractmethod
    def handle(self, message: Message) -> Response:
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


class KeepAlive(ConsumerCommand):
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


class SendMessage(ConsumerCommand):
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


class Version(QueryCommand):
    def __init__(self) -> None:
        super().__init__("version")

    def handle(self, message: Message) -> Response:
        version = message.param("version")

        if version is None:
            raise errors.MessageError("version failed")

        return Response(version)


class Whoami(QueryCommand):
    def __init__(self) -> None:
        super().__init__("whoami")

    def handle(self, message: Message) -> Response:
        client_id = message.param("client_id")

        if client_id is None:
            raise errors.MessageError("whoami failed")

        return Response(client_id)
