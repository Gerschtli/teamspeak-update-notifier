from __future__ import annotations

import queue
import time
from types import TracebackType
from typing import TYPE_CHECKING, List, Optional, Type

from . import commands, errors, handlers

if TYPE_CHECKING:
    from .message import Message


class Client:
    def __init__(self, queue_read: "queue.Queue[Message]", queue_write: "queue.Queue[Message]") -> None:
        self._queue_read = queue_read
        self._queue_write = queue_write
        self._last_message_sent = 0

    def execute(self, command: commands.Command) -> Optional[commands.Response]:
        self._queue_write.put(command.message)
        self._last_message_sent = int(time.time())

        result = None
        if isinstance(command, commands.QueryCommand):
            result = command.handle(self._queue_read.get())

        command.check_error(self._queue_read.get())

        return result

    def listen(self, handlers_list: List[handlers.Handler]) -> None:
        keep_alive = commands.KeepAlive()

        while True:
            # ts3 server expects a message at least every 5 min, so to be sure send every 4 min
            if time.time() - self._last_message_sent > 4 * 60:
                self.execute(keep_alive)

            try:
                message = self._queue_read.get(timeout=30)
            except queue.Empty:
                continue

            if message is None:
                continue

            for handler in handlers_list:
                if handler.match(message):
                    command = handler.execute(message)
                    if command is not None:
                        self.execute(command)
                    break

    def __enter__(self) -> Client:
        # skip first two lines
        self._queue_read.get()
        self._queue_read.get()

        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]],  # type: ignore
                 exception_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        connection_errors = [errors.SocketConnectionError, errors.ServerDisconnectError]
        if exception_type not in connection_errors:
            self.execute(commands.Quit())

        return False
