from logging import getLogger
from typing import Optional, Union

import lineage.dataclasses.adf as dataclasses
from reader.file import json
from search.pipeline import find_copy_activities

LOGGER = getLogger(__name__)


class Adf:
    def __init__(self, dataclass: Union[dataclasses.Pipeline, dataclasses.Dataset]):
        self.dataclass = dataclass

    @classmethod
    def from_jsonfile(cls, file_path: str):

        json_data: Optional[dict] = json(
            file_path=file_path,
            logger=LOGGER,
        )

        if cls.__name__ == "Pipeline" and json_data:
            pipeline_dataclass = dataclasses.Pipeline(
                file_path=file_path,
                json_data=json_data,
            )
            return cls(dataclass=pipeline_dataclass)

        if cls.__name__ == "Dataset" and json_data:
            dataset_dataclass = dataclasses.Dataset(
                name=json_data.get("name", None),
                file_path=file_path,
                json_data=json_data,
                linked_service_name=json_data.get("properties", {})
                .get("linkedServiceName", {})
                .get("referenceName", None),
            )
            return cls(dataclass=dataset_dataclass)


class Pipeline(Adf):
    def __init__(
        self,
        dataclass: dataclasses.Pipeline = dataclasses.Pipeline(
            file_path=None,
            json_data=None,
        ),
    ):
        super().__init__(dataclass=dataclass)
        self.pipeline: dataclasses.Pipeline = dataclass
        self.copy_activities: list[dataclasses.CopyActivity] = find_copy_activities(
            pipeline=dataclass
        )


class Dataset(Adf):
    def __init__(
        self,
        dataclass: dataclasses.Dataset = dataclasses.Dataset(
            name=None,
            file_path=None,
            json_data=None,
            linked_service_name=None,
        ),
    ):
        super().__init__(dataclass=dataclass)
        self.dataset: dataclasses.Dataset = dataclass
