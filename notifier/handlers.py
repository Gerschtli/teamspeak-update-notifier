import logging
from abc import abstractmethod

from . import commands, errors, version_manager
from .client import Client
from .message import Message

LOGGER: logging.Logger = logging.getLogger(__name__)


class Handler:
    @staticmethod
    @abstractmethod
    def match(message: Message) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def execute(self, client: Client, message: Message) -> None:
        raise NotImplementedError()


class ClientEnter(Handler):
    def __init__(self, server_group_id: str, current_version: str) -> None:
        self._server_group_id = server_group_id
        self._current_version = current_version

    @staticmethod
    def match(message: Message) -> bool:
        return message.command == "notifycliententerview"

    def execute(self, client: Client, message: Message) -> None:
        client_id = message.param("clid")
        servergroups = message.param("client_servergroups")
        nickname = message.param("client_nickname")

        LOGGER.debug("client %s (id: %s) with server group %s entered", nickname, client_id,
                     servergroups)

        if (servergroups != self._server_group_id
                or client_id is None
                or nickname is None
                or not version_manager.need_update(self._current_version)):
            return

        client.execute(commands.SendMessage(client_id, version_manager.build_message()))

        LOGGER.info("send message to client %s", nickname)


class ClientLeft(Handler):
    def __init__(self, client_id: str) -> None:
        self._client_id = client_id

    @staticmethod
    def match(message: Message) -> bool:
        return message.command == "notifyclientleftview"

    def execute(self, client: Client, message: Message) -> None:
        # check for server down
        if message.param("reasonid") == "11":
            raise errors.ServerDisconnectError("server shutdown received")

        # check for client disconnect
        if message.param("clid") == self._client_id:
            raise errors.ServerDisconnectError("client disconnected")
