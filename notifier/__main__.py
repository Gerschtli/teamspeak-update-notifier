import signal
import sys
import types

from . import app, commands, errors, handlers
from .client import Client


def _start() -> None:
    signal.signal(signal.SIGTERM, _sigterm_handler)

    with Client() as client:
        client.execute(commands.Login())
        client.execute(commands.Use())

        whoami = client.execute(commands.Whoami())
        if whoami is None or whoami.client_id is None:
            raise errors.MessageError("whoami failed")

        client.execute(commands.NotifyRegister())

        client.listen(
            [handlers.ClientEnter(),
             handlers.ClientLeft(whoami.client_id)])


# pylint: disable=no-member
def _sigterm_handler(_signo: signal.Signals,
                     _stack_frame: types.FrameType) -> None:
    raise errors.SigTermError("process killed via SIGTERM")


def main() -> None:
    try:
        _start()
    except KeyboardInterrupt:
        app.LOGGER.info("exit cause: keyboard interrupt")
        sys.exit(errors.SigTermError.exit_code)
    except errors.Error as error:
        app.LOGGER.info("exit cause: %s", error)
        sys.exit(error.exit_code)


if __name__ == "__main__":
    main()
