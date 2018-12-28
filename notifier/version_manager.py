from bs4 import BeautifulSoup  # type: ignore
import requests

from .app import CONFIG, LOGGER
from .commands import SendMessage
from .socket import Socket

DOWNLOAD_LINK: str = ("https://www.teamspeak.de/download/"
                      "teamspeak-3-amd64-server-linux/")


def need_update() -> bool:
    current_version = CONFIG.get("notifier", "current_version")
    recent_version = _recent_version()
    result = current_version != recent_version

    LOGGER.debug("current version {} - recent version {} - update {}".format(
        current_version, recent_version, result))

    return result


def send_message(socket: Socket, client_id: str, nickname: str) -> None:
    message = "Please update your server to version {}!".format(
        _recent_version())

    socket.write(SendMessage(client_id, message))

    LOGGER.info("send message to client {}".format(nickname))


def _recent_version() -> str:
    data = requests.get(DOWNLOAD_LINK)

    soup = BeautifulSoup(data.text, "html.parser")  # type: ignore
    element = soup.select("[itemprop=softwareVersion]")  # type: ignore
    version: str = element[0].text  # type: ignore

    return version
