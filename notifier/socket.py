from __future__ import annotations

import logging
import queue
import socket
import threading
from abc import abstractmethod
from contextlib import contextmanager
from typing import Any, Iterator

from . import errors
from .message import Message

BUFFER_SIZE: int = 2048
LOGGER: logging.Logger = logging.getLogger(__name__)
MESSAGE_END: str = "\n\r"
TIMEOUT_SECONDS: int = 10


@contextmanager
def init_socket(host: str, port: int) -> Iterator[socket.socket]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            LOGGER.info("socket connected")
        except socket.error:
            raise errors.SocketConnectionError("socket connect failed") from socket.error

        yield sock


class SocketThread(threading.Thread):
    def __init__(self, sock: socket.socket, queue_: "queue.Queue[Message]", *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._sock = sock
        self._queue = queue_
        self.__killed = False

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError()

    def kill(self) -> None:
        self.__killed = True

    def run(self) -> None:
        while not self.__killed:
            self.execute()


class SocketReader(SocketThread):
    def __init__(self, sock: socket.socket, queue_: "queue.Queue[Message]", *args: Any, **kwargs: Any):
        super().__init__(sock, queue_, *args, **kwargs)
        self._sock.settimeout(TIMEOUT_SECONDS)  # return recv after timeout

    def execute(self) -> None:
        try:
            data_raw = self._sock.recv(BUFFER_SIZE)
        except socket.timeout:
            return

        data_decoded = data_raw.decode().rstrip(MESSAGE_END)

        for message_raw in data_decoded.split(MESSAGE_END):
            LOGGER.debug("read message: %s", message_raw)
            message = Message.build_from_string(message_raw)

            if message is not None:
                self._queue.put(message)


class SocketWriter(SocketThread):
    def execute(self) -> None:
        try:
            message = self._queue.get(timeout=TIMEOUT_SECONDS)
        except queue.Empty:
            return

        LOGGER.debug("write message: %s", message)
        message_string = str(message) + MESSAGE_END
        self._sock.send(message_string.encode())
