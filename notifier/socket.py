from typing import Optional, List
import socket
from logging import Logger

from .errors import SocketConnectionError
from .message import Message


class Socket:
    received_buffer: List[str] = []
    buffer_size: int = 2048
    last_message: Optional[Message] = None
    message_end: str = "\n\r"

    def __init__(self, logger: Logger, host: str, port: str) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = logger
        self.host = host
        self.port = int(port)

    def close(self) -> None:
        self.socket.close()
        self.logger.info("socket closed")

    def connect(self) -> None:
        try:
            self.socket.connect((self.host, self.port))
            self.logger.info("socket connected")
        except socket.error:
            self.logger.exception("socket connect failed")
            raise SocketConnectionError("socket connect failed")

    def read(self, ignore: bool = False) -> Optional[Message]:
        if self.received_buffer:
            return self.read_from_buffer(ignore)

        message_raw = self.socket.recv(self.buffer_size)
        message_decoded = message_raw.decode("utf-8")
        message = message_decoded.rstrip(self.message_end)
        messages = message.split(self.message_end)

        self.received_buffer.extend(messages)

        return self.read_from_buffer(ignore)

    def read_from_buffer(self, ignore: bool = False) -> Optional[Message]:
        message = self.received_buffer.pop(0)
        if ignore:
            self.logger.debug("ignoring message: {}".format(message))
            return None

        self.logger.debug("read message: {}".format(message))
        return Message.build_from_string(message)

    def write(self, message: Message) -> None:
        self.logger.debug("write message: {}".format(message))
        self.last_message = message
        message_string = str(message) + self.message_end
        self.socket.send(str.encode(message_string))
