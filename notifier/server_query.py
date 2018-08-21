from time import sleep
import sys
from .message import Message


class ServerQuery:
    def __init__(self, socket, version_manager, logger, username, password,
                 server_id, server_group_id):
        self.socket = socket
        self.version_manager = version_manager
        self.logger = logger
        self.username = username
        self.password = password
        self.server_id = server_id
        self.server_group_id = server_group_id

    def check_ok(self):
        message = self.socket.read()
        if message.command == "error" and message.param("msg") == "ok":
            return

        self.logger.error("an error occured performing '{}': {}".format(
            self.socket.last_message, message))
        sys.exit(2)

    def close(self):
        self.socket.write(Message("quit"))
        self.socket.close()
        self.logger.info("server query closed")

    def connect(self):
        if not self.socket.connect():
            self.logger.error("socket not conntected")
            sys.exit(1)

        self.socket.read(ignore=True)  # ignore initial messages
        self.socket.read(ignore=True)  # ignore initial messages
        self.socket.write(
            Message(
                "login", {
                    "client_login_name": self.username,
                    "client_login_password": self.password
                }))
        self.check_ok()

        self.socket.write(Message("use", {"sid": self.server_id}))
        self.check_ok()

        self.logger.info("server query connected")

    def handle_client_enter(self, message):
        client_id = message.param("clid")
        servergroups = message.param("client_servergroups")
        nickname = message.param("client_nickname")

        self.logger.debug(
            "client {} (id: {}) with server group {} entered".format(
                nickname, client_id, servergroups))

        if servergroups != self.server_group_id \
                or not self.version_manager.need_update():
            return

        message = "Please update your server to version {}!".format(
            self.version_manager.recent_version())

        self.socket.write(
            Message("sendtextmessage", {
                "targetmode": "1",
                "target": client_id,
                "msg": message
            }))
        self.socket.read(ignore=True)  # ignore notifytextmessage
        self.check_ok()

        self.logger.info("send message to client {}".format(nickname))

    def handle_client_left(self, message, current_client_id):
        # check for server down
        if message.param("reasonid") == "11":
            self.logger.info("server shutdown received")
            sys.exit(3)

        # check for client disconnect
        if message.param("clid") == current_client_id:
            self.logger.info("client disconnected")
            sys.exit(3)

    def current_client_id(self):
        self.socket.write(Message("whoami"))
        message = self.socket.read()
        self.check_ok()

        client_id = message.param("client_id")
        self.logger.debug("current client id: {}".format(client_id))

        return client_id

    def notifier(self):
        current_client_id = self.current_client_id()

        self.socket.write(Message("servernotifyregister", {"event": "server"}))
        self.check_ok()

        while True:
            sleep(1)

            message = self.socket.read()
            if message is None:
                self.logger.error("empty message received")
                sys.exit(3)

            self.logger.info("received {}".format(message.command))

            if message.command == "notifycliententerview":
                self.handle_client_enter(message)
            elif message.command == "notifyclientleftview":
                self.handle_client_left(message, current_client_id)
