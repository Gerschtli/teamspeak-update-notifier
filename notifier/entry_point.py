import signal

from .errors import MessageError, SigTermError
from .client import Client
from .commands import CommandFactory
from .handlers import HandlerFactory


def start(client: Client, command_factory: CommandFactory,
          handler_factory: HandlerFactory) -> None:
    signal.signal(signal.SIGTERM, _sigterm_handler)  # type: ignore

    client.quit_command = command_factory.quit()
    with client:
        client.flush_initial_messages()

        client.execute(command_factory.login())
        client.execute(command_factory.use())
        whoami = client.execute(command_factory.whoami())
        if whoami is None or whoami.client_id is None:
            raise MessageError("whoami failed")
        client.execute(command_factory.notify_register())

        client.handlers.append(handler_factory.client_enter())
        client.handlers.append(handler_factory.client_left(whoami.client_id))
        client.listen()


def _sigterm_handler(_signo, _stack_frame):  # type: ignore
    raise SigTermError("process killed via SIGTERM")
