from configparser import ConfigParser
from .container import IocContainer
import argparse
# import logging

from .logger import log_info


def main():
    # parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to config file.")
    args = parser.parse_args()

    # load config
    config = ConfigParser()
    config.read(args.config)
    config_dict = {s: dict(config.items(s)) for s in config.sections()}
    log_info("loaded config")

    # set up container
    container = IocContainer(config=config_dict)
    # container.logger().addHandler(logging.StreamHandler(sys.stdout))

    container.entry_point()
