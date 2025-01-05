from glob import glob
from json import load
from logging import Logger, getLogger
from os import path
from typing import List, Optional

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


def pipelines_from_directory(dir_path: str) -> List[str]:
    json_files: List[str] = glob(path.join(dir_path, "*.json"))
    return json_files
