from bs4 import BeautifulSoup
import requests
import time
from .logger import log_debug, log_info


class VersionManager:
    cache_time = 86400  # one day in seconds
    last_updated = None
    version = None

    def __init__(self, current_version):
        self.current_version = current_version

    def need_update(self):
        recent_version = self.recent_version()
        result = self.current_version != self.recent_version()

        log_debug("current version {} - recent version {} - update {}".format(
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

        log_info("updated recent version cache")

        return version
