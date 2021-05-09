import argparse
import configparser
import logging
import queue
from typing import TYPE_CHECKING

from . import commands, handlers
from .client import Client
from .socket import SocketReader, SocketWriter, init_socket

if TYPE_CHECKING:
    from .message import Message

LOGGER: logging.Logger = logging.getLogger(__name__)


def build_config() -> configparser.ConfigParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to config file.")
    config_path: str = parser.parse_args().config

    config = configparser.ConfigParser()
    config.read(config_path)

    return config


def start(config: configparser.ConfigParser) -> None:
    config_ts3 = dict(config.items("ts3"))
    config_notifier = dict(config.items("notifier"))

    with init_socket(config_ts3["host"], int(config_ts3["port"])) as sock:
        queue_read: "queue.Queue[Message]" = queue.Queue()
        queue_write: "queue.Queue[Message]" = queue.Queue()

        reader = SocketReader(sock, queue_read)
        writer = SocketWriter(sock, queue_write)

        reader.start()
        writer.start()

        try:
            with Client(queue_read, queue_write) as client:
                client.execute(commands.Login(config_ts3["username"], config_ts3["password"]))
                client.execute(commands.Use(config_ts3["server_id"]))

                whoami = client.query(commands.Whoami())
                version = client.query(commands.Version())

                client.execute(commands.NotifyRegister())

                client.listen([
                    handlers.ClientEnter(config_notifier["server_group_id"],
                                         version.result),
                    handlers.ClientLeft(whoami.result)
                ])
        finally:
            reader.kill()
            writer.kill()
            LOGGER.debug("waiting for threads")
            reader.join(timeout=20)
            writer.join(timeout=20)
