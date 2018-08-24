from collections import namedtuple

from .errors import MessageError, ServerDisconnectError


class HandlerFactory:
    def __init__(self, logger, notifier, socket, version_manager,
                 server_group_id):
        self.logger = logger
        self.notifier = notifier
        self.socket = socket
        self.version_manager = version_manager
        self.server_group_id = server_group_id

    def client_enter(self):
        return ClientEnter(
            self.logger,
            self.notifier,
            self.version_manager,
            self.server_group_id,
        )

    def client_left(self, client_id):
        return ClientLeft(client_id)

    def error(self):
        return Error(self.socket)

    def whoami(self):
        return Whoami()


class ClientEnter:
    def __init__(self, logger, notifier, version_manager, server_group_id):
        self.logger = logger
        self.notifier = notifier
        self.version_manager = version_manager
        self.server_group_id = server_group_id

    def match(self, message):
        return message.command == "notifycliententerview"

    def execute(self, message):
        client_id = message.param("clid")
        servergroups = message.param("client_servergroups")
        nickname = message.param("client_nickname")

        self.logger.debug(
            "client {} (id: {}) with server group {} entered".format(
                nickname, client_id, servergroups))

        if (servergroups != self.server_group_id
                or not self.version_manager.need_update()):
            return

        version = self.version_manager.recent_version()
        self.notifier.send_message(client_id, nickname, version)


class ClientLeft:
    def __init__(self, client_id):
        self.client_id = client_id

    def match(self, message):
        return message.command == "notifyclientleftview"

    def execute(self, message):
        # check for server down
        if message.param("reasonid") == "11":
            raise ServerDisconnectError("server shutdown received")

        # check for client disconnect
        if message.param("clid") == self.client_id:
            raise ServerDisconnectError("client disconnected")


class Error:
    def __init__(self, socket):
        self.socket = socket

    def execute(self, message):
        if message.command == "error" and message.param("msg") == "ok":
            return

        raise MessageError("error in command: {}".format(
            self.socket.last_message))


class Whoami:
    return_value = True

    def execute(self, message):
        WhoamiResponse = namedtuple("WhoamiResponse", ["client_id"])

        return WhoamiResponse(message.param("client_id"))
