from logging import Logger, getLogger
from typing import List, Optional, Union

import lineage.dataclasses.adf as dataclasses
from reader.file import json
from search.pipeline import find_copy_activities, find_pipeline_parameters

LOGGER = getLogger(__name__)


class Adf:
    def __init__(
        self,
        data: Union[
            dataclasses.Pipeline,
            dataclasses.Dataset,
            dataclasses.LinkedService,
        ],
    ):
        self.data = data

    @classmethod
    def from_jsonfile(cls, file_path: str):

        json_data: Optional[dict] = json(
            file_path=file_path,
            logger=LOGGER,
        )

        if cls.__name__ == "Pipeline" and json_data:
            return cls(
                data=dataclasses.Pipeline(
                    name=json_data.get("name", None),
                    file_path=file_path,
                    json_data=json_data,
                )
            )

        if cls.__name__ == "Dataset" and json_data:
            return cls(
                data=dataclasses.Dataset(
                    name=json_data.get("name", None),
                    file_path=file_path,
                    json_data=json_data,
                    linked_service_name=json_data.get("properties", {})
                    .get("linkedServiceName", {})
                    .get("referenceName", None),
                )
            )

        if cls.__name__ == "LinkedService" and json_data:
            return cls(
                data=dataclasses.LinkedService(
                    name=json_data.get("name", None),
                    file_path=file_path,
                    json_data=json_data,
                )
            )


class Pipeline(Adf):
    def __init__(
        self,
        data: dataclasses.Pipeline = dataclasses.Pipeline(
            name=None,
            file_path=None,
            json_data=None,
        ),
        logger: Logger = LOGGER,
    ):
        super().__init__(data=data)
        self.logger = logger
        self.copy_activities: list[dataclasses.CopyActivity] = []

        if isinstance(self.data, dataclasses.Pipeline):
            self.copy_activities = find_copy_activities(pipeline=self.data)

        self.parameters: List[dataclasses.PipelineParameter] = (
            self.find_pipeline_parameters()
        )

    def find_pipeline_parameters(self) -> List[dataclasses.PipelineParameter]:
        if isinstance(self.data, dataclasses.Pipeline):
            self.parameters = find_pipeline_parameters(pipeline=self.data)

        return self.parameters


class Dataset(Adf):
    def __init__(
        self,
        data: dataclasses.Dataset = dataclasses.Dataset(
            name=None,
            file_path=None,
            json_data=None,
            linked_service_name=None,
        ),
    ):
        super().__init__(data=data)


class LinkedService(Adf):
    def __init__(
        self,
        data: dataclasses.LinkedService = dataclasses.LinkedService(
            name=None,
            file_path=None,
            json_data=None,
        ),
    ):
        super().__init__(data=data)
