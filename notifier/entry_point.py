import signal

from .errors import SigTermError


def start(client, command_factory, handler_factory):
    signal.signal(signal.SIGTERM, _sigterm_handler)

    client.quit_command = command_factory.quit()
    with client:
        client.flush_initial_messages()

        client.execute(command_factory.login())
        client.execute(command_factory.use())
        whoami = client.execute(command_factory.whoami())
        client.execute(command_factory.notify_register())

        client.handlers.append(handler_factory.client_enter())
        client.handlers.append(handler_factory.client_left(whoami.client_id))
        client.listen()


def _sigterm_handler(_signo, _stack_frame):
    raise SigTermError("process killed via SIGTERM")
