import bs4  # type: ignore
import requests

from . import app, commands
from .socket import Socket

DOWNLOAD_LINK: str = ("https://www.teamspeak.de/download/teamspeak-3-amd64-server-linux/")


def need_update(current_version: str) -> bool:
    recent_version = _recent_version()
    result = current_version != recent_version

    app.LOGGER.debug("current version %s - recent version %s - update %s", current_version, recent_version, result)

    return result


def send_message(socket: Socket, client_id: str, nickname: str) -> None:
    message = "Please update your server to version {}!".format(_recent_version())

    socket.write(commands.SendMessage(client_id, message))

    app.LOGGER.info("send message to client %s", nickname)


def _recent_version() -> str:
    data = requests.get(DOWNLOAD_LINK)

    soup = bs4.BeautifulSoup(data.text, "html.parser")
    element = soup.select("[itemprop=softwareVersion]")
    version: str = element[0].text

    return version
