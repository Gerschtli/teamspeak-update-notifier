import signal
import sys


def start(server_query):
    signal.signal(signal.SIGTERM, sigterm_handler)

    try:
        server_query.connect()
        server_query.notifier()
    finally:
        server_query.close()


def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    sys.exit(0)
