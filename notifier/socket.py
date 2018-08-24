import socket

from .errors import ConnectionError
from .message import Message


class Socket:
    received_buffer = []
    buffer_size = 2048
    last_message = None
    message_end = "\n\r"

    def __init__(self, logger, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = logger
        self.host = host
        self.port = int(port)

    def close(self):
        self.socket.close()
        self.logger.info("socket closed")

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            self.logger.info("socket connected")
        except socket.error as error:
            self.logger.exception("socket connect failed")
            raise ConnectionError("socket connect failed")

    def read(self, ignore=False):
        if len(self.received_buffer) > 0:
            return self.read_from_buffer(ignore)

        message = self.socket.recv(self.buffer_size)
        message = message.decode("utf-8")
        message = message.rstrip(self.message_end)
        messages = message.split(self.message_end)

        self.received_buffer.extend(messages)

        return self.read_from_buffer(ignore)

    def read_from_buffer(self, ignore=False):
        message = self.received_buffer.pop(0)
        if ignore:
            self.logger.debug("ignoring message: {}".format(message))
            return

        self.logger.debug("read message: {}".format(message))
        return Message.build_from_string(message)

    def write(self, message):
        self.logger.debug("write message: {}".format(message))
        self.last_message = message
        message_string = str(message) + self.message_end
        self.socket.send(str.encode(message_string))
