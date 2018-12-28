from logging import Logger
from types import TracebackType
from typing import List, Optional, Type

from .commands import Quit, SendMessage, Whoami
from .errors import SocketConnectionError, ServerDisconnectError
from .handlers import Handler, HandlerFactory, WhoamiResponse
from .message import Message
from .socket import Socket


class Client:
    handlers: List[Handler] = []
    quit_command: Optional[Quit] = None

    def __init__(self, handler_factory: HandlerFactory, logger: Logger,
                 socket: Socket) -> None:
        self.handler_factory = handler_factory
        self.logger = logger
        self.socket = socket

    def execute(self, command: Message) -> Optional[WhoamiResponse]:
        self.socket.write(command)

        if isinstance(command, SendMessage):
            self.skip_messages(1)

        result = None
        if isinstance(command, Whoami):
            message = self.socket.read()
            if message is not None:
                result = self.handler_factory.whoami().execute(message)

        message = self.socket.read()
        if message is not None:
            self.handler_factory.error().execute(message)

        return result

    def flush_initial_messages(self) -> None:
        self.skip_messages(2)

    def listen(self) -> None:
        while True:
            message = self.socket.read()
            if message is None:
                continue

            for handler in self.handlers:
                if handler.match(message):
                    handler.execute(message)
                    break

    def skip_messages(self, count: int) -> None:
        for _ in range(count):
            self.socket.read(ignore=True)

    def __enter__(self) -> 'Client':
        self.socket.connect()

        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]],
                 exception_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        should_quit = exception_type not in [
            SocketConnectionError, ServerDisconnectError
        ]
        if should_quit and self.quit_command is not None:
            self.execute(self.quit_command)

        self.socket.close()

        return False
