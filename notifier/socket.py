import logging
import socket
from typing import List, Optional

from . import errors
from .message import Message

BUFFER_SIZE: int = 2048
LOGGER: logging.Logger = logging.getLogger(__name__)
MESSAGE_END: str = "\n\r"


class Socket:
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._received_buffer: List[str] = []
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.last_command: Optional[Message] = None

    def close(self) -> None:
        self._socket.close()
        LOGGER.info("socket closed")

    def connect(self) -> None:
        try:
            self._socket.connect((self._host, self._port))
            LOGGER.info("socket connected")
        except socket.error:
            LOGGER.exception("socket connect failed")
            raise errors.SocketConnectionError("socket connect failed")

    def read(self, ignore: bool = False) -> Optional[Message]:
        if self._received_buffer:
            return self.read_from_buffer(ignore)

        message_raw = self._socket.recv(BUFFER_SIZE)
        message_decoded = message_raw.decode()
        message = message_decoded.rstrip(MESSAGE_END)
        messages = message.split(MESSAGE_END)

        self._received_buffer.extend(messages)

        return self.read_from_buffer(ignore)

    def read_from_buffer(self, ignore: bool = False) -> Optional[Message]:
        message = self._received_buffer.pop(0)
        if ignore:
            LOGGER.debug("ignoring message: %s", message)
            return None

        LOGGER.debug("read message: %s", message)
        return Message.build_from_string(message)

    def write(self, message: Message) -> None:
        LOGGER.debug("write message: %s", message)
        self.last_command = message
        message_string = str(message) + MESSAGE_END
        self._socket.send(str.encode(message_string))
