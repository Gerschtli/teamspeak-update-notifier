from dependency_injector import containers, providers
import logging

from .entry_point import start
from .socket import Socket
from .server_query import ServerQuery
from .version_manager import VersionManager


class IocContainer(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    logger = providers.Singleton(logging.Logger, name="notifier")

    socket = providers.Singleton(
        Socket, logger=logger, host=config.ts3.host, port=config.ts3.port)

    version_manager = providers.Singleton(
        VersionManager,
        logger=logger,
        current_version=config.notifier.current_version)

    server_query = providers.Singleton(
        ServerQuery,
        socket=socket,
        version_manager=version_manager,
        logger=logger,
        username=config.ts3.username,
        password=config.ts3.password,
        server_id=config.ts3.server_id,
        server_group_id=config.notifier.server_group_id)

    entry_point = providers.Callable(
        start,
        server_query=server_query,
    )