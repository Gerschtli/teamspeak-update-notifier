import logging
import signal
import sys
import types

from . import app, errors

logger = logging.getLogger(__name__)


# pylint: disable=no-member
def _sigterm_handler(_signo: signal.Signals, _stack_frame: types.FrameType) -> None:
    raise errors.SigTermError("process killed via SIGTERM")


def _handle_exception(exception: BaseException, exit_code: int) -> None:
    logger.exception("exception occured in main, stopping application")
    sys.exit(exit_code)


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout,
    )

    config = app.build_config()
    signal.signal(signal.SIGTERM, _sigterm_handler)

    try:
        app.start(config)
    except KeyboardInterrupt as exception:
        _handle_exception(exception, errors.SigTermError.exit_code)
    except errors.Error as exception:
        _handle_exception(exception, exception.exit_code)
