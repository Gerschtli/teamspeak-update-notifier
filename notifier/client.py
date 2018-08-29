from .commands import SendMessage, Whoami
from .errors import SocketConnectionError, ServerDisconnectError


class Client:
    handlers = []
    quit_command = None

    def __init__(self, handler_factory, logger, socket):
        self.handler_factory = handler_factory
        self.logger = logger
        self.socket = socket

    def execute(self, command):
        self.socket.write(command)

        if isinstance(command, SendMessage):
            self.skip_messages(1)

        result = None
        if isinstance(command, Whoami):
            message = self.socket.read()
            result = self.handler_factory.whoami().execute(message)

        message = self.socket.read()
        self.handler_factory.error().execute(message)

        return result

    def flush_initial_messages(self):
        self.skip_messages(2)

    def listen(self):
        while True:
            message = self.socket.read()

            for handler in self.handlers:
                if handler.match(message):
                    handler.execute(message)
                    break

    def skip_messages(self, count):
        for __ in range(count):
            self.socket.read(ignore=True)

    def __enter__(self):
        self.socket.connect()

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        should_quit = exception_type not in [
            SocketConnectionError, ServerDisconnectError
        ]
        if should_quit and self.quit_command is not None:
            self.execute(self.quit_command)

        self.socket.close()
