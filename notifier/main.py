import logging
import signal
import sys
import types
from typing import Optional

from . import app, errors

LOGGER: logging.Logger = logging.getLogger(__name__)


# pylint: disable=no-member
def _sigterm_handler(_signo: int, _stack_frame: Optional[types.FrameType]) -> None:
    raise errors.SigTermError("process killed via SIGTERM")


def _handle_exception(exit_code: int) -> None:
    LOGGER.exception("exception occurred in main, stopping application")
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
    except KeyboardInterrupt:
        _handle_exception(errors.SigTermError.exit_code)
    except errors.Error as exception:
        _handle_exception(exception.exit_code)
