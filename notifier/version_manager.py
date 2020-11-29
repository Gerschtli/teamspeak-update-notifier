import logging

import bs4  # type: ignore
import requests

DOWNLOAD_LINK: str = "https://www.teamspeak.de/download/teamspeak-3-amd64-server-linux/"
LOGGER: logging.Logger = logging.getLogger(__name__)


def build_message() -> str:
    return "Please update your server to version {}!".format(_recent_version())


def need_update(current_version: str) -> bool:
    recent_version = _recent_version()
    result = current_version != recent_version

    LOGGER.debug("current version %s - recent version %s - update %s", current_version,
                 recent_version, result)

    return result


def _recent_version() -> str:
    data = requests.get(DOWNLOAD_LINK)

    soup = bs4.BeautifulSoup(data.text, "html.parser")
    element = soup.select("[itemprop=softwareVersion]")
    version: str = element[0].text

    return version
