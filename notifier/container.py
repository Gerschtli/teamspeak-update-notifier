from dependency_injector import containers, providers
import logging

from .client import Client
from .commands import CommandFactory
from .handlers import HandlerFactory
from .entry_point import start
from .socket import Socket
from .version_manager import Notifier, VersionManager


class IocContainer(containers.DeclarativeContainer):
    config = providers.Configuration("config")
    logger = providers.Singleton(logging.Logger, name="notifier")

    socket = providers.Singleton(
        Socket,
        logger=logger,
        host=config.ts3.host,
        port=config.ts3.port,
    )

    version_manager = providers.Singleton(
        VersionManager,
        logger=logger,
        current_version=config.notifier.current_version,
    )

    command_factory = providers.Singleton(
        CommandFactory,
        username=config.ts3.username,
        password=config.ts3.password,
        server_id=config.ts3.server_id,
    )

    notifier = providers.Singleton(
        Notifier,
        command_factory=command_factory,
        logger=logger,
        socket=socket,
    )

    handler_factory = providers.Singleton(
        HandlerFactory,
        logger=logger,
        notifier=notifier,
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
