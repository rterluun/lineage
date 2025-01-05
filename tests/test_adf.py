import lineage.dataclasses.adf as dataclasses
from lineage.adf import Dataset, LinkedService, Pipeline, Pipelines


def test_pipeline_from_jsonfile(adf_pipeline: Pipeline):
    pipeline = Pipeline().from_jsonfile(file_path="tests/data/pipelines/pipeline.json")
    assert pipeline.data == adf_pipeline


def test_pipeline_copy_activities(
    adf_pipeline: dataclasses.Pipeline,
    adf_copy_activity: dataclasses.CopyActivity,
):
    pipeline = Pipeline(data=adf_pipeline)
    assert pipeline.copy_activities == adf_copy_activity


def test_dataset_from_jsonfile(adf_dataset: Dataset):
    dataset = Dataset().from_jsonfile(file_path="tests/data/datasets/dataset.json")
    assert dataset.data == adf_dataset


def test_linkedservice_from_jsonfile(adf_linkedservice: dataclasses.LinkedService):
    linkedservice = LinkedService().from_jsonfile(
        file_path="tests/data/linkedservices/linkedservice.json"
    )
    assert linkedservice.data == adf_linkedservice


def test_pipelines_from_directory():
    assert (
        Pipelines().from_directory(dir_path="tests/data/pipelines").pipelines.dir_path
        == "tests/data/pipelines"
    )
