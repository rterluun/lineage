from json import load
from logging import Logger, getLogger
from typing import Optional

LOGGER = getLogger(__name__)


def json(file_path: str, logger: Logger = LOGGER):

    json_data: Optional[dict] = None

    try:
        with open(file_path) as f:
            json_data = dict(load(f))
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except TypeError:
        logger.error(f"Error reading file: {file_path}")

    return json_data
