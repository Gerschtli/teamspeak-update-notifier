from logging import Logger
from typing import Callable, Optional
import time

from bs4 import BeautifulSoup  # type: ignore
import requests

from .commands import CommandFactory
from .socket import Socket


def cache_version(original_function: Callable[['VersionManager'], str]
                  ) -> Callable[['VersionManager'], str]:
    def new_function(self: 'VersionManager') -> str:
        current_timestamp = time.time()
        if (self.version is not None and self.last_updated is not None
                and self.last_updated > current_timestamp - self.cache_time):
            return self.version

        version = original_function(self)

        self.version = version
        self.last_updated = current_timestamp

        self.logger.info("updated recent version cache")

        return version

    return new_function


class VersionManager:
    cache_time: int = 86400  # one day in seconds
    last_updated: Optional[float] = None
    link: str = \
        "https://www.teamspeak.de/download/teamspeak-3-amd64-server-linux/"
    version: Optional[str] = None

    def __init__(self, command_factory: CommandFactory, logger: Logger,
                 socket: Socket, current_version: str) -> None:
        self.command_factory = command_factory
        self.logger = logger
        self.socket = socket
        self.current_version = current_version

    def need_update(self) -> bool:
        recent_version = self.recent_version()
        result = self.current_version != self.recent_version()

        self.logger.debug(
            "current version {} - recent version {} - update {}".format(
                self.current_version, recent_version, result))

        return result

    def send_message(self, client_id: str, nickname: str) -> None:
        message = "Please update your server to version {}!".format(
            self.recent_version())

        self.socket.write(
            self.command_factory.send_message(client_id, message))

        self.logger.info("send message to client {}".format(nickname))

    @cache_version
    def recent_version(self) -> str:
        data = requests.get(self.link)

        soup = BeautifulSoup(data.text, "html.parser")  # type: ignore
        element = soup.select("[itemprop=softwareVersion]")  # type: ignore
        version: str = element[0].text  # type: ignore

        return version
