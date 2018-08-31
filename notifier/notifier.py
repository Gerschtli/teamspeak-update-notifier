import logging
import sys

import argparse
from configparser import ConfigParser

from .container import IocContainer
from .errors import Error, SigTermError


def main():
    # parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to config file.")
    args = parser.parse_args()

    # load config
    config = ConfigParser()
    config.read(args.config)
    config_dict = {s: dict(config.items(s)) for s in config.sections()}

    # set up container
    container = IocContainer(config=config_dict)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("[{levelname}] {message}", style="{"))
    # handler.setLevel(logging.INFO)
    container.logger().addHandler(handler)

    # run application
    try:
        container.entry_point()
    except KeyboardInterrupt:
        container.logger().info("exit cause: keyboard interrupt")
        sys.exit(SigTermError.exit_code)
    except Error as error:
        container.logger().info("exit cause: {}".format(error))
        sys.exit(error.exit_code)
