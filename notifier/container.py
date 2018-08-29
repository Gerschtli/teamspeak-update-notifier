import logging

from dependency_injector import containers, providers

from .client import Client
from .commands import CommandFactory
from .entry_point import start
from .handlers import HandlerFactory
from .socket import Socket
from .version_manager import VersionManager


class IocContainer(containers.DeclarativeContainer):
    # pylint: disable=no-member

    config = providers.Configuration("config")
    logger = providers.Singleton(logging.Logger, name="notifier")

    socket = providers.Singleton(
        Socket,
        logger=logger,
        host=config.ts3.host,
        port=config.ts3.port,
    )

    command_factory = providers.Singleton(
        CommandFactory,
        username=config.ts3.username,
        password=config.ts3.password,
        server_id=config.ts3.server_id,
    )

    version_manager = providers.Singleton(
        VersionManager,
        command_factory=command_factory,
        logger=logger,
        socket=socket,
        current_version=config.notifier.current_version,
    )

    handler_factory = providers.Singleton(
        HandlerFactory,
        logger=logger,
        socket=socket,
        version_manager=version_manager,
        server_group_id=config.notifier.server_group_id,
    )

    client = providers.Singleton(
        Client,
        handler_factory=handler_factory,
        logger=logger,
        socket=socket,
    )

    entry_point = providers.Callable(
        start,
        client=client,
        command_factory=command_factory,
        handler_factory=handler_factory,
    )
