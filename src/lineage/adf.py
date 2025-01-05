from logging import Logger, getLogger
from typing import List, Optional, Union

import lineage.dataclasses.adf as dataclasses
from reader.file import json, pipelines_from_directory
from search.pipeline import find_copy_activities

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


class Pipelines:

    def __init__(
        self,
        pipelines: Optional[dataclasses.Pipelines] = None,
    ):
        self.pipelines: Optional[dataclasses.Pipelines] = pipelines

    @classmethod
    def from_directory(cls, dir_path: str):
        pipeline_files: List[str] = pipelines_from_directory(dir_path=dir_path)
        pipelines: List[dataclasses.Pipeline] = []

        for file_path in pipeline_files:
            pipelines.append(Pipeline.from_jsonfile(file_path=file_path))

        return cls(
            pipelines=dataclasses.Pipelines(
                dir_path=dir_path,
                pipelines=pipelines,
            )
        )
