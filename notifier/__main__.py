import configparser
import signal
import sys
import types

from . import app, commands, errors, handlers
from .client import Client
from .socket import Socket


def _start(config: configparser.ConfigParser) -> None:
    config_ts3 = dict(config.items("ts3"))
    config_notifier = dict(config.items("notifier"))

    socket = Socket(config_ts3["host"], int(config_ts3["port"]))
    with Client(socket) as client:
        client.execute(commands.Login(config_ts3["username"], config_ts3["password"]))
        client.execute(commands.Use(config_ts3["server_id"]))

        whoami = client.execute(commands.Whoami())
        if whoami is None or whoami.client_id is None:
            raise errors.MessageError("whoami failed")

        client.execute(commands.NotifyRegister())

        client.listen([
            handlers.ClientEnter(config_notifier["server_group_id"], config_notifier["current_version"]),
            handlers.ClientLeft(whoami.client_id)
        ])


# pylint: disable=no-member
def _sigterm_handler(_signo: signal.Signals, _stack_frame: types.FrameType) -> None:
    raise errors.SigTermError("process killed via SIGTERM")


def main() -> None:
    config = app.build_config()
    signal.signal(signal.SIGTERM, _sigterm_handler)

    try:
        _start(config)
    except KeyboardInterrupt:
        app.LOGGER.info("exit cause: keyboard interrupt")
        sys.exit(errors.SigTermError.exit_code)
    except errors.Error as error:
        app.LOGGER.info("exit cause: %s", error)
        sys.exit(error.exit_code)


if __name__ == "__main__":
    main()
