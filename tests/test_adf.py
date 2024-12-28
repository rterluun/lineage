import lineage.dataclasses.adf as dataclasses
from lineage.adf import Dataset, Pipeline


def test_pipeline_from_jsonfile(adf_pipeline: Pipeline):
    pipeline = Pipeline().from_jsonfile(file_path="tests/data/pipeline.json")
    assert pipeline.pipeline == adf_pipeline


def test_pipeline_copy_activities(
    adf_pipeline: dataclasses.Pipeline,
    adf_copy_activity: dataclasses.CopyActivity,
):
    pipeline = Pipeline(dataclass=adf_pipeline)
    assert pipeline.copy_activities == adf_copy_activity


def test_dataset_from_jsonfile(adf_dataset: Dataset):
    dataset = Dataset().from_jsonfile(file_path="tests/data/dataset.json")
    assert dataset.dataset == adf_dataset


# def test_pipeline_calls_dataset(
#     adf_pipeline: dataclasses.Pipeline,
#     adf_dataset: dataclasses.Dataset,
#     call_datasets: list[dataclasses.CallDataset],
# ):
#     pipeline = Pipeline(dataclass=adf_pipeline, datasets=[adf_dataset])
#     assert pipeline.calls_dataset == call_datasets
