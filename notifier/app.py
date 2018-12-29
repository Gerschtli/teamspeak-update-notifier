import argparse
import configparser
import logging
import sys

LOGGER_NAME: str = "notifier"


def _setup_config() -> configparser.ConfigParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to config file.")
    config_path: str = parser.parse_args().config

    config = configparser.ConfigParser()
    config.read(config_path)

    return config


def _setup_logger() -> logging.Logger:
    formatter = logging.Formatter("[{levelname}] {message}", style="{")

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    # handler.setLevel(logging.INFO)

    logger = logging.Logger(name=LOGGER_NAME)
    logger.addHandler(handler)

    return logger


CONFIG = _setup_config()
LOGGER = _setup_logger()
