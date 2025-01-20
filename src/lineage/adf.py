from logging import Logger, getLogger
from typing import List, Optional, Union

import lineage.dataclasses.adf as dataclasses
from lineage.dataclasses.metadata import Metadata
from reader.file import json
from search.pipeline import (
    find_copy_activities,
    find_pipeline_parameters,
    find_pipeline_reference_activities,
    replace_activity_parameters_with_values,
    update_pipeline_parameters,
)

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
    def from_jsonfile(
        cls,
        file_path: str,
        metadata: Optional[Metadata] = None,
    ):

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
                    metadata=metadata,
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
                    metadata=metadata,
                )
            )

        if cls.__name__ == "LinkedService" and json_data:
            return cls(
                data=dataclasses.LinkedService(
                    name=json_data.get("name", None),
                    file_path=file_path,
                    json_data=json_data,
                    metadata=metadata,
                )
            )


class Pipeline(Adf):
    def __init__(
        self,
        data: dataclasses.Pipeline = dataclasses.Pipeline(
            name=None,
            file_path=None,
            json_data=None,
            metadata=None,
        ),
        logger: Logger = LOGGER,
        replace_parameters: bool = False,
        execute_pipeline_parameters: Optional[
            List[dataclasses.PipelineParameter]
        ] = None,
    ):
        super().__init__(data=data)
        self.logger = logger
        self.replace_parameters = replace_parameters
        self.execute_pipeline_parameters = execute_pipeline_parameters
        self.parameters: List[dataclasses.PipelineParameter] = (
            self.find_pipeline_parameters()
        )
        self.copy_activities: List[dataclasses.CopyActivity] = (
            self.find_copy_activities()
        )
        self.pipeline_reference_activities: List[dataclasses.PipelineReference] = (
            self.find_pipeline_reference_activities()
        )

    def find_pipeline_parameters(self) -> List[dataclasses.PipelineParameter]:
        parameters: List[dataclasses.PipelineParameter] = []

        if isinstance(self.data, dataclasses.Pipeline):
            parameters = find_pipeline_parameters(pipeline=self.data)

            if self.execute_pipeline_parameters:
                parameters = update_pipeline_parameters(
                    parameters=parameters,
                    updated_parameters=self.execute_pipeline_parameters,
                )

        return parameters

    def find_copy_activities(self) -> List[dataclasses.CopyActivity]:
        copy_activities: List[dataclasses.CopyActivity] = []

        if isinstance(self.data, dataclasses.Pipeline):
            copy_activities = find_copy_activities(pipeline=self.data)

            if self.replace_parameters:
                copy_activities = replace_activity_parameters_with_values(
                    activities=copy_activities,
                    parameters=self.parameters,
                )

        return copy_activities

    def find_pipeline_reference_activities(self) -> List[dataclasses.PipelineReference]:
        pipeline_reference_activities: List[dataclasses.PipelineReference] = []

        if isinstance(self.data, dataclasses.Pipeline):
            pipeline_reference_activities = find_pipeline_reference_activities(
                pipeline=self.data
            )

        return pipeline_reference_activities


class Dataset(Adf):
    def __init__(
        self,
        data: dataclasses.Dataset = dataclasses.Dataset(
            name=None,
            file_path=None,
            json_data=None,
            linked_service_name=None,
            metadata=None,
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
            metadata=None,
        ),
    ):
        super().__init__(data=data)
