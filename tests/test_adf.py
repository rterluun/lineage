from typing import List

import lineage.dataclasses.adf as dataclasses
from lineage.adf import Dataset, LinkedService, Pipeline


def test_pipeline_from_jsonfile(adf_pipeline: Pipeline):
    pipeline = Pipeline().from_jsonfile(file_path="tests/data/pipeline.json")
    assert pipeline.data == adf_pipeline


def test_pipeline_copy_activities(
    adf_pipeline: dataclasses.Pipeline,
    adf_copy_activity: dataclasses.CopyActivity,
):
    pipeline = Pipeline(data=adf_pipeline)
    assert pipeline.copy_activities == adf_copy_activity


def test_dataset_from_jsonfile(adf_dataset: Dataset):
    dataset = Dataset().from_jsonfile(file_path="tests/data/dataset.json")
    assert dataset.data == adf_dataset


def test_linkedservice_from_jsonfile(adf_linkedservice: dataclasses.LinkedService):
    linkedservice = LinkedService().from_jsonfile(
        file_path="tests/data/linkedservice.json"
    )
    assert linkedservice.data == adf_linkedservice


def test_pipeline_parameters(
    adf_pipeline: dataclasses.Pipeline,
    adf_pipeline_parameters: List[dataclasses.PipelineParameter],
):
    pipeline = Pipeline(data=adf_pipeline)
    assert pipeline.parameters == adf_pipeline_parameters


def test_pipeline_copy_activities_replace_parameters(
    adf_pipeline: dataclasses.Pipeline,
):
    pipeline = Pipeline(
        data=adf_pipeline,
        replace_parameters=True,
    )

    assert [
        activity for activity in pipeline.copy_activities if activity.name == "Copy 2"
    ] == [
        dataclasses.CopyActivity(
            name="Copy 2",
            inputs=[
                {
                    "referenceName": "DS_REST",
                    "type": "DatasetReference",
                    "parameters": {},
                }
            ],
            outputs=[
                {
                    "referenceName": "dataset",
                    "type": "DatasetReference",
                    "parameters": {"pFolder": {"value": "raw", "type": "Expression"}},
                }
            ],
            inputs_dataset_name="DS_REST",
            outputs_dataset_name="dataset",
        )
    ]
