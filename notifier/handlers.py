from abc import abstractmethod
from logging import Logger
from typing import NamedTuple, Optional

from .errors import MessageError, ServerDisconnectError
from .message import Message
from .socket import Socket
from .version_manager import VersionManager


class Handler:
    @staticmethod
    @abstractmethod
    def match(message: Message) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def execute(self, message: Message) -> None:
        raise NotImplementedError()


class ClientEnter(Handler):
    def __init__(self, logger: Logger, version_manager: VersionManager,
                 server_group_id: str) -> None:
        self.logger = logger
        self.version_manager = version_manager
        self.server_group_id = server_group_id

    @staticmethod
    def match(message: Message) -> bool:
        return message.command() == "notifycliententerview"

    def execute(self, message: Message) -> None:
        client_id = message.param("clid")
        servergroups = message.param("client_servergroups")
        nickname = message.param("client_nickname")

        self.logger.debug(
            "client {} (id: {}) with server group {} entered".format(
                nickname, client_id, servergroups))

        if (servergroups != self.server_group_id
                or not self.version_manager.need_update() or client_id is None
                or nickname is None):
            return

        self.version_manager.send_message(client_id, nickname)


class ClientLeft(Handler):
    def __init__(self, client_id: str) -> None:
        self.client_id = client_id

    @staticmethod
    def match(message: Message) -> bool:
        return message.command() == "notifyclientleftview"

    def execute(self, message: Message) -> None:
        # check for server down
        if message.param("reasonid") == "11":
            raise ServerDisconnectError("server shutdown received")

        # check for client disconnect
        if message.param("clid") == self.client_id:
            raise ServerDisconnectError("client disconnected")


class Error:
    def __init__(self, socket: Socket) -> None:
        self.socket = socket

    def execute(self, message: Message) -> None:
        if message.command() == "error" and message.param("msg") == "ok":
            return

        raise MessageError("error in command: {}".format(
            self.socket.last_message))


class WhoamiResponse(NamedTuple):
    client_id: Optional[str]


class Whoami:
    @staticmethod
    def execute(message: Message) -> WhoamiResponse:
        return WhoamiResponse(message.param("client_id"))


class HandlerFactory:
    def __init__(self, logger: Logger, socket: Socket,
                 version_manager: VersionManager,
                 server_group_id: str) -> None:
        self.logger = logger
        self.socket = socket
        self.version_manager = version_manager
        self.server_group_id = server_group_id

    def client_enter(self) -> ClientEnter:
        return ClientEnter(
            self.logger,
            self.version_manager,
            self.server_group_id,
        )

    @staticmethod
    def client_left(client_id: str) -> ClientLeft:
        return ClientLeft(client_id)

    def error(self) -> Error:
        return Error(self.socket)

    @staticmethod
    def whoami() -> Whoami:
        return Whoami()
