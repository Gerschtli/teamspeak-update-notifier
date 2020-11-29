from __future__ import annotations

import queue
from types import TracebackType
from typing import List, Optional, Type, TypeVar

from . import commands, errors, handlers

T = TypeVar('T')


class Client:
    def __init__(self, queue_read: queue.Queue, queue_write: queue.Queue) -> None:
        self._queue_read = queue_read
        self._queue_write = queue_write

    def execute(self, command: commands.Command) -> Optional[T]:
        self._queue_write.put(command.message)

        result = None
        if isinstance(command, commands.QueryCommand):
            result = command.handle(self._queue_read.get())

        command.check_error(self._queue_read.get())

        return result

    def listen(self, handlers_list: List[handlers.Handler]) -> None:
        while True:
            message = self._queue_read.get()
            if message is None:
                continue

            for handler in handlers_list:
                if handler.match(message):
                    handler.execute(self, message)
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
