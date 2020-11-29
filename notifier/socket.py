from __future__ import annotations

import logging
import socket
from types import TracebackType
from typing import List, Optional, Type

from . import commands, errors
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

    def read(self, ignore: bool = False) -> Optional[Message]:
        if self._received_buffer:
            return self.read_from_buffer(ignore)

        message_raw = self.recv()
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

    def recv(self):
        while True:
            try:
                return self._socket.recv(BUFFER_SIZE)
            except socket.timeout:
                self.write(commands.KeepAlive())

    def write(self, message: Message) -> None:
        LOGGER.debug("write message: %s", message)
        self.last_command = message
        message_string = str(message) + MESSAGE_END
        self._socket.send(str.encode(message_string))

    def __enter__(self) -> Socket:
        try:
            self._socket.connect((self._host, self._port))

            # timeout is 4 min because after 5 min of inactivity the connection gets closed
            self._socket.settimeout(4 * 60)

            LOGGER.info("socket connected")
        except socket.error:
            LOGGER.exception("socket connect failed")
            raise errors.SocketConnectionError("socket connect failed")

        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]],  # type: ignore
                 exception_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        self._socket.close()
        LOGGER.info("socket closed")

        return False
