from types import TracebackType
from typing import List, Optional, Type

from .commands import Quit, SendMessage, Whoami
from .errors import SocketConnectionError, ServerDisconnectError
from .handlers import Handler, WhoamiResponse, handle_error, handle_whoami
from .message import Message
from .socket import Socket


class Client:
    def __init__(self) -> None:
        self._socket = Socket()

    def execute(self, command: Message) -> Optional[WhoamiResponse]:
        self._socket.write(command)

        if isinstance(command, SendMessage):
            self._skip_messages(1)

        result = None
        if isinstance(command, Whoami):
            message = self._socket.read()
            if message is not None:
                result = handle_whoami(message)

        message = self._socket.read()
        if message is not None:
            handle_error(message)

        return result

    def listen(self, handlers: List[Handler]) -> None:
        while True:
            message = self._socket.read()
            if message is None:
                continue

            for handler in handlers:
                if handler.match(message):
                    handler.execute(self._socket, message)
                    break

    def _skip_messages(self, count: int) -> None:
        for _ in range(count):
            self._socket.read(ignore=True)

    def __enter__(self) -> 'Client':
        self._socket.connect()
        self._skip_messages(2)

        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]],
                 exception_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        connection_errors = [SocketConnectionError, ServerDisconnectError]
        if exception_type not in connection_errors:
            self.execute(Quit())

        self._socket.close()

        return False
