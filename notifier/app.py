import argparse
import configparser

from . import commands, errors, handlers
from .client import Client
from .socket import Socket


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

    with Socket(config_ts3["host"], int(config_ts3["port"])) as socket:
        with Client(socket) as client:
            client.execute(commands.Login(config_ts3["username"], config_ts3["password"]))
            client.execute(commands.Use(config_ts3["server_id"]))

            whoami = client.execute(commands.Whoami())
            if whoami is None or whoami.client_id is None:
                raise errors.MessageError("whoami failed")

            client.execute(commands.NotifyRegister())

            client.listen([
                handlers.ClientEnter(config_notifier["server_group_id"],
                                     config_notifier["current_version"]),
                handlers.ClientLeft(whoami.client_id)
            ])
