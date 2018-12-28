import argparse
from configparser import ConfigParser
import logging
import sys

LOGGER_NAME = "notifier"


def _setup_config() -> ConfigParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to config file.")
    config_path: str = parser.parse_args().config

    config = ConfigParser()
    config.read(config_path)

    return config


def _setup_logger() -> logging.Logger:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("[{levelname}] {message}", style="{"))
    # handler.setLevel(logging.INFO)

    logger = logging.Logger(name=LOGGER_NAME)
    logger.addHandler(handler)

    return logger


CONFIG = _setup_config()
LOGGER = _setup_logger()
