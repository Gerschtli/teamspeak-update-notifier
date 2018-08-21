from time import sleep
import sys
from .logger import log_debug, log_error, log_info
from .message import Message


class ServerQuery:
    def __init__(self, socket):
        self.socket = socket

    def check_ok(self):
        message = self.socket.read()
        if message.command == "error" and message.param("msg") == "ok":
            return

        log_error("an error occured performing '{}': {}".format(
            self.socket.last_message, message))
        sys.exit(2)

    def close(self):
        self.socket.write(Message("quit"))
        self.socket.close()
        log_info("server query closed")

    def connect(self, username, password, server_id):
        self.socket.read(ignore=True)  # ignore initial messages
        self.socket.read(ignore=True)  # ignore initial messages
        self.socket.write(
            Message("login", {
                "client_login_name": username,
                "client_login_password": password
            }))
        self.check_ok()

        self.socket.write(Message("use", {"sid": server_id}))
        self.check_ok()

        log_info("server query connected")

    def handle_client_enter(self, message, server_group_id, version_manager):
        client_id = message.param("clid")
        servergroups = message.param("client_servergroups")
        nickname = message.param("client_nickname")

        log_debug("client {} (id: {}) with server group {} entered".format(
            nickname, client_id, servergroups))

        if servergroups != server_group_id \
                or not version_manager.need_update():
            return

        message = "Please update your server to version {}!".format(
            version_manager.recent_version())

        self.socket.write(
            Message("sendtextmessage", {
                "targetmode": "1",
                "target": client_id,
                "msg": message
            }))
        self.socket.read(ignore=True)  # ignore notifytextmessage
        self.check_ok()

        log_info("send message to client {}".format(nickname))

    def handle_client_left(self, message, current_client_id):
        # check for server down
        if message.param("reasonid") == "11":
            log_info("server shutdown received")
            sys.exit(3)

        # check for client disconnect
        if message.param("clid") == current_client_id:
            log_info("client disconnected")
            sys.exit(3)

    def current_client_id(self):
        self.socket.write(Message("whoami"))
        message = self.socket.read()
        self.check_ok()

        client_id = message.param("client_id")
        log_debug("current client id: {}".format(client_id))

        return client_id

    def notifier(self, server_group_id, version_manager):
        current_client_id = self.current_client_id()

        self.socket.write(Message("servernotifyregister", {"event": "server"}))
        self.check_ok()

        while True:
            sleep(1)

            message = self.socket.read()
            if message is None:
                log_error("empty message received")
                sys.exit(3)

            log_info("received {}".format(message.command))

            if message.command == "notifycliententerview":
                self.handle_client_enter(message, server_group_id,
                                         version_manager)
            elif message.command == "notifyclientleftview":
                self.handle_client_left(message, current_client_id)
