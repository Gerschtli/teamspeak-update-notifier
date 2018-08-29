import time

from bs4 import BeautifulSoup
import requests


def cache_version(original_function):
    def new_function(self):
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
    cache_time = 86400  # one day in seconds
    last_updated = None
    link = "https://www.teamspeak.de/download/teamspeak-3-amd64-server-linux/"
    version = None

    def __init__(self, command_factory, logger, socket, current_version):
        self.command_factory = command_factory
        self.logger = logger
        self.socket = socket
        self.current_version = current_version

    def need_update(self):
        recent_version = self.recent_version()
        result = self.current_version != self.recent_version()

        self.logger.debug(
            "current version {} - recent version {} - update {}".format(
                self.current_version, recent_version, result))

        return result

    def send_message(self, client_id, nickname):
        message = "Please update your server to version {}!".format(
            self.recent_version())

        self.socket.write(
            self.command_factory.send_message(client_id, message))

        self.logger.info("send message to client {}".format(nickname))

    @cache_version
    def recent_version(self):
        data = requests.get(self.link)

        soup = BeautifulSoup(data.text, "html.parser")
        version = soup.select("[itemprop=softwareVersion]")[0].text

        return version
