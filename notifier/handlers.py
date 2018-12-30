import logging
from abc import abstractmethod
from typing import NamedTuple, Optional

from . import errors, version_manager
from .message import Message
from .socket import Socket

logger = logging.getLogger(__name__)


class Handler:
    @staticmethod
    @abstractmethod
    def match(message: Message) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def execute(self, socket: Socket, message: Message) -> None:
        raise NotImplementedError()


class ClientEnter(Handler):
    def __init__(self, server_group_id: str, current_version: str) -> None:
        self._server_group_id = server_group_id
        self._current_version = current_version

    @staticmethod
    def match(message: Message) -> bool:
        return message.command == "notifycliententerview"

    def execute(self, socket: Socket, message: Message) -> None:
        client_id = message.param("clid")
        servergroups = message.param("client_servergroups")
        nickname = message.param("client_nickname")

        logger.debug("client %s (id: %s) with server group %s entered", nickname, client_id,
                     servergroups)

        if (servergroups != self._server_group_id or client_id is None or nickname is None
                or not version_manager.need_update(self._current_version)):
            return

        version_manager.send_message(socket, client_id, nickname)


class ClientLeft(Handler):
    def __init__(self, client_id: str) -> None:
        self._client_id = client_id

    @staticmethod
    def match(message: Message) -> bool:
        return message.command == "notifyclientleftview"

    def execute(self, socket: Socket, message: Message) -> None:
        # check for server down
        if message.param("reasonid") == "11":
            raise errors.ServerDisconnectError("server shutdown received")

        # check for client disconnect
        if message.param("clid") == self._client_id:
            raise errors.ServerDisconnectError("client disconnected")


class WhoamiResponse(NamedTuple):
    client_id: Optional[str]


def handle_error(message: Message, last_command: Optional[Message]) -> None:
    if message is not None and message.command == "error" and message.param("msg") == "ok":
        return

    raise errors.MessageError("error last command: {}".format(last_command))


def handle_whoami(message: Message) -> WhoamiResponse:
    return WhoamiResponse(message.param("client_id"))
