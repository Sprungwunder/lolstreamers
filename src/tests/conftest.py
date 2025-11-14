import logging
import sys

import pytest


@pytest.fixture(autouse=True, scope="session")
def api_logging_to_console():
    """
    Send only `api.*` logs to console during pytest.
    """
    # Parent logger for your package; children like `api.league` inherit this
    logger = logging.getLogger("api")

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)

    logger.handlers = [handler]
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # No restoration – applies for the whole pytest process
    yield
