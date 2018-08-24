from bs4 import BeautifulSoup
import requests
import time


class VersionManager:
    cache_time = 86400  # one day in seconds
    last_updated = None
    version = None

    def __init__(self, logger, current_version):
        self.logger = logger
        self.current_version = current_version

    def need_update(self):
        recent_version = self.recent_version()
        result = self.current_version != self.recent_version()

        self.logger.debug(
            "current version {} - recent version {} - update {}".format(
                self.current_version, recent_version, result))

        return result

    def recent_version(self):
        current_timestamp = time.time()
        if self.version is not None \
                and self.last_updated is not None \
                and self.last_updated > current_timestamp - self.cache_time:
            return self.version

        link = "https://www.teamspeak.de/download/teamspeak-3-amd64-server-linux/"
        data = requests.get(link)

        soup = BeautifulSoup(data.text, "html.parser")
        version = soup.select("[itemprop=softwareVersion]")[0].text

        self.version = version
        self.last_updated = current_timestamp

        self.logger.info("updated recent version cache")

        return version


class Notifier:
    def __init__(self, command_factory, logger, socket):
        self.command_factory = command_factory
        self.logger = logger
        self.socket = socket

    def send_message(self, client_id, nickname, version):
        message = "Please update your server to version {}!".format(version)

        self.socket.write(
            self.command_factory.send_message(client_id, message))

        self.logger.info("send message to client {}".format(nickname))
