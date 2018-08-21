import socket
from .logger import log_debug, log_info
from .message import Message


class Socket:
    received_buffer = []
    buffer_size = 2048
    last_message = None
    message_end = "\n\r"

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = int(port)

    def close(self):
        self.socket.close()
        log_info("socket closed")

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            log_info("socket connected")
            return True
        except:
            return False

    def read(self, ignore=False):
        if len(self.received_buffer) > 0:
            message = self.received_buffer.pop(0)
            return None if ignore else Message.build_from_string(message)

        message = self.socket.recv(self.buffer_size)
        message = message.decode("utf-8")
        message = message.rstrip(self.message_end)
        messages = message.split(self.message_end)

        if len(messages) > 1:
            self.received_buffer.extend(messages[1:])

        log_debug("read message: {}".format(messages[0]))
        return None if ignore else Message.build_from_string(messages[0])

    def write(self, message):
        log_debug("write message: {}".format(message))
        self.last_message = message
        message_string = str(message) + self.message_end
        self.socket.send(str.encode(message_string))
