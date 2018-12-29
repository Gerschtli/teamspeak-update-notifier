from types import TracebackType
from typing import List, Optional, Type

from . import commands, errors, handlers, socket
from .message import Message


class Client:
    def __init__(self) -> None:
        self._socket = socket.Socket()

    def execute(self, command: Message) -> Optional[handlers.WhoamiResponse]:
        self._socket.write(command)

        if isinstance(command, commands.SendMessage):
            self._skip_messages(1)

        result = None
        if isinstance(command, commands.Whoami):
            message = self._socket.read()
            if message is not None:
                result = handlers.handle_whoami(message)

        message = self._socket.read()
        if message is not None:
            handlers.handle_error(message)

        return result

    def listen(self, handlers_list: List[handlers.Handler]) -> None:
        while True:
            message = self._socket.read()
            if message is None:
                continue

            for handler in handlers_list:
                if handler.match(message):
                    handler.execute(self._socket, message)
                    break

    def _skip_messages(self, count: int) -> None:
        for _ in range(count):
            self._socket.read(ignore=True)

    def __enter__(self) -> "Client":
        self._socket.connect()
        self._skip_messages(2)

        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]], exception_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        connection_errors = [errors.SocketConnectionError, errors.ServerDisconnectError]
        if exception_type not in connection_errors:
            self.execute(commands.Quit())

        self._socket.close()

        return False
