import logging
import sys

import argparse
from configparser import ConfigParser

from .container import IocContainer
from .errors import Error, SigTermError


def main() -> None:
    # parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to config file.")
    configPath: str = parser.parse_args().config

    # load config
    config = ConfigParser()
    config.read(configPath)
    config_dict = {s: dict(config.items(s)) for s in config.sections()}

    # set up container
    container = IocContainer(config=config_dict)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("[{levelname}] {message}", style="{"))
    # handler.setLevel(logging.INFO)

    logger: logging.Logger = container.logger()  # type: ignore
    logger.addHandler(handler)

    # run application
    try:
        container.entry_point()
    except KeyboardInterrupt:
        logger.info("exit cause: keyboard interrupt")
        sys.exit(SigTermError.exit_code)
    except Error as error:
        logger.info("exit cause: {}".format(error))
        sys.exit(error.exit_code)
