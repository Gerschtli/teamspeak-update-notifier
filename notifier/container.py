import logging
from typing import Callable

from dependency_injector import containers, providers  # type: ignore

from .client import Client
from .commands import CommandFactory
from .entry_point import start
from .handlers import HandlerFactory
from .socket import Socket
from .version_manager import VersionManager


class IocContainer(containers.DeclarativeContainer):  # type: ignore
    # pylint: disable=no-member

    config = providers.Configuration("config")  # type: ignore
    logger: logging.Logger = providers.Singleton(  # type: ignore
        logging.Logger, name="notifier")

    socket: Socket = providers.Singleton(  # type: ignore
        Socket,
        logger=logger,
        host=config.ts3.host,  # type: ignore
        port=config.ts3.port,  # type: ignore
    )

    command_factory: CommandFactory = providers.Singleton(  # type: ignore
        CommandFactory,
        username=config.ts3.username,  # type: ignore
        password=config.ts3.password,  # type: ignore
        server_id=config.ts3.server_id,  # type: ignore
    )

    version_manager: VersionManager = providers.Singleton(  # type: ignore
        VersionManager,
        command_factory=command_factory,
        logger=logger,
        socket=socket,
        current_version=config.notifier.current_version,  # type: ignore
    )

    handler_factory: HandlerFactory = providers.Singleton(  # type: ignore
        HandlerFactory,
        logger=logger,
        socket=socket,
        version_manager=version_manager,
        server_group_id=config.notifier.server_group_id,  # type: ignore
    )

    client: Client = providers.Singleton(  # type: ignore
        Client,
        handler_factory=handler_factory,
        logger=logger,
        socket=socket,
    )

    entry_point: Callable[['IocContainer'],
                          None] = providers.Callable(  # type: ignore
                              start,
                              client=client,
                              command_factory=command_factory,
                              handler_factory=handler_factory,
                          )
