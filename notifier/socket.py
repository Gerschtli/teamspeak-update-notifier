from typing import Optional, List
import socket

from .app import CONFIG, LOGGER
from .errors import SocketConnectionError
from .message import Message

BUFFER_SIZE: int = 2048
MESSAGE_END: str = "\n\r"


class Socket:
    def __init__(self) -> None:
        self._received_buffer: List[str] = []
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self) -> None:
        self._socket.close()
        LOGGER.info("socket closed")

    def connect(self) -> None:
        try:
            host = CONFIG.get("ts3", "host")
            port = int(CONFIG.get("ts3", "port"))
            self._socket.connect((host, port))
            LOGGER.info("socket connected")
        except socket.error:
            LOGGER.exception("socket connect failed")
            raise SocketConnectionError("socket connect failed")

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
            LOGGER.debug("ignoring message: {}".format(message))
            return None

        LOGGER.debug("read message: {}".format(message))
        return Message.build_from_string(message)

    def write(self, message: Message) -> None:
        LOGGER.debug("write message: {}".format(message))
        message_string = str(message) + MESSAGE_END
        self._socket.send(str.encode(message_string))
