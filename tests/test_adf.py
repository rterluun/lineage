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


def test_pipeline_calls_pipeline(
    adf_pipeline_exec_pipeline: dataclasses.Pipeline,
    adf_pipeline_reference_activities: List[dataclasses.PipelineReference],
):
    pipeline = Pipeline(data=adf_pipeline_exec_pipeline)
    assert pipeline.pipeline_reference_activities == adf_pipeline_reference_activities
