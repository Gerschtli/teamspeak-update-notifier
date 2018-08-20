from time import sleep
import sys
from .logger import log_debug, log_error, log_info

class ServerQuery:
    def __init__(self, socket):
        self.socket = socket

    def check_ok(self):
        message = self.socket.read()
        if message != "error id=0 msg=ok":
            log_error("an error occured performing '{}': {}".format(self.socket.last_message, message))
            sys.exit(2)

    def close(self):
        self.socket.write("quit")
        self.socket.close()
        log_info("server query closed")

    def connect(self, username, password, server_id):
        self.socket.read() # ignore initial messages
        self.socket.read() # ignore initial messages
        self.socket.write("login {} {}".format(username, password))
        self.check_ok()

        self.socket.write("use {}".format(server_id))
        self.check_ok()

        log_info("server query connected")

    def handle_client_enter(self, message_parts, server_group_id, version_manager):
        client_id = None
        servergroups = None
        nickname = None

        for part in message_parts:
            if part.startswith("clid="):
                client_id = part.lstrip("clid=")
            elif part.startswith("client_nickname="):
                nickname = part.lstrip("client_nickname=")
            elif part.startswith("client_servergroups="):
                servergroups = part.lstrip("client_servergroups=")

        log_debug("client {} (id: {}) with server group {} entered".format(nickname, client_id, servergroups))

        if servergroups != str(server_group_id) or not version_manager.need_update():
            return

        message = "Please update your server to version {}!".format(version_manager.recent_version())
        message = message.replace(" ", "\s")
        self.socket.write("sendtextmessage targetmode=1 target={} msg={}".format(client_id, message))
        self.socket.read() # ignore notifytextmessage
        self.check_ok()

        log_info("send message to client {}".format(nickname))

    def handle_client_left(self, message_parts, current_client_id):
        # check for server down
        if "reasonid=11" in message_parts:
            log_info("server shutdown received")
            sys.exit(3)

        # check for client disconnect
        if "clid=".format(current_client_id) in message_parts:
            log_info("client disconnected")
            sys.exit(3)

    def notifier(self, server_group_id, version_manager):
        self.socket.write("whoami")
        message = self.socket.read()
        self.check_ok()
        message_parts = message.split(" ")

        current_client_id = None
        for part in message_parts:
            if part.startswith("client_id="):
                current_client_id = part.lstrip("client_id=")

        log_debug("current client id: {}".format(current_client_id))

        self.socket.write("servernotifyregister event=server")
        self.check_ok()

        while True:
            sleep(1)

            message = self.socket.read()
            if message == "":
                log_error("empty message received")
                sys.exit(3)

            message_parts = message.split(" ")

            log_info("received {}".format(message_parts[0]))

            if message_parts[0] == "notifycliententerview":
                self.handle_client_enter(message_parts, server_group_id, version_manager)
            elif message_parts[0] == "notifyclientleftview":
                self.handle_client_left(message_parts, current_client_id)
