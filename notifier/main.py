import logging
import signal
import sys
import types

from . import app, errors

logger = logging.getLogger(__name__)


# pylint: disable=no-member
def _sigterm_handler(_signo: signal.Signals, _stack_frame: types.FrameType) -> None:
    raise errors.SigTermError("process killed via SIGTERM")


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
        logger.info("exit cause: keyboard interrupt")
        sys.exit(errors.SigTermError.exit_code)
    except errors.Error as error:
        logger.info("exit cause: %s", error)
        sys.exit(error.exit_code)
