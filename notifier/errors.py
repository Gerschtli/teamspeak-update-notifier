class Error(Exception):
    exit_code = 127


class SocketConnectionError(Error):
    exit_code = 1


class MessageError(Error):
    exit_code = 2


class ServerDisconnectError(Error):
    exit_code = 3


class SigTermError(Error):
    exit_code = 4
