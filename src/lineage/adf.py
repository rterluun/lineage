from logging import Logger, getLogger
from typing import Optional

import lineage.dataclasses.adf as dataclasses
from reader.file import json
from search.pipeline import find_copy_activities

LOGGER = getLogger(__name__)


class Pipeline:
    def __init__(
        self,
        pipeline: dataclasses.Pipeline = dataclasses.Pipeline(
            file_path=None, json_data=None
        ),
        logger: Logger = LOGGER,
    ):
        self.pipeline: dataclasses.Pipeline = pipeline
        self.logger = logger
        self.copy_activities: list[dataclasses.CopyActivity] = (
            find_copy_activities(  # noqa: E501
                pipeline=pipeline,
                logger=logger,
            )
        )

    @classmethod
    def from_jsonfile(cls, file_path: str):
        json_data: Optional[dict] = json(file_path=file_path)

        return cls(
            pipeline=dataclasses.Pipeline(
                file_path=file_path,
                json_data=json_data,
            )
        )
