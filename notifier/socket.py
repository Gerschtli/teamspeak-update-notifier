import socket
from .logger import log_debug, log_error, log_info


class Socket:
    buffer_size = 2048
    is_connected = False
    last_message = None
    message_end = "\n\r"

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self):
        self.socket.close()
        log_info("socket closed")

    def connect(self, host, port):
        self.socket.connect((host, port))
        self.is_connected = True
        log_info("socket connected")

    def read(self):
        message = self.socket.recv(self.buffer_size)
        message = message.decode("utf-8")
        message = message.rstrip(self.message_end)
        log_debug("read message: {}".format(message))
        return message

    def write(self, message):
        log_debug("write message: {}".format(message))
        self.last_message = message
        message += self.message_end
        self.socket.send(str.encode(message))
