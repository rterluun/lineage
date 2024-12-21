from typing import Optional

import lineage.dataclasses.adf as dataclasses
from reader.file import json


class Pipeline:
    def __init__(
        self,
        pipeline: dataclasses.Pipeline = dataclasses.Pipeline(
            file_path=None, json_data=None
        ),
    ):
        self.pipeline: dataclasses.Pipeline = pipeline

    @classmethod
    def from_jsonfile(cls, file_path: str):
        json_data: Optional[dict] = json(file_path=file_path)

        return cls(
            pipeline=dataclasses.Pipeline(
                file_path=file_path,
                json_data=json_data,
            )
        )
