from configparser import ConfigParser
import argparse
import signal
import sys

from .socket import Socket
from .server_query import ServerQuery
from .version_manager import VersionManager
from .logger import log_error, log_info


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to config file.")
    args = parser.parse_args()

    conf = ConfigParser()
    conf.read(args.config)
    log_info("loaded config")

    signal.signal(signal.SIGTERM, sigterm_handler)

    try:
        custom_socket = Socket()
        custom_socket.connect(
            conf.get("ts3", "host"),
            conf.getint("ts3", "port")
        )
    except:
        custom_socket.close()

    if not custom_socket.is_connected:
        log_error("socket not conntected")
        sys.exit(1)

    try:
        server_query = ServerQuery(custom_socket)
        server_query.connect(
            conf.get("ts3", "username"),
            conf.get("ts3", "password"),
            conf.get("ts3", "server_id")
        )

        version_manager = VersionManager(
            conf.get("notifier", "current_version")
        )

        server_query.notifier(
            conf.get("notifier", "server_group_id"),
            version_manager
        )
    finally:
        server_query.close()


def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    sys.exit(0)
