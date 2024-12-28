from json import load

import pytest

from lineage.dataclasses.adf import CopyActivity, Dataset, LinkedService, Pipeline

with open("tests/data/pipeline.json") as f:
    pipeline_json_data = dict(load(f))

with open("tests/data/dataset.json") as f:
    dataset_json_data = dict(load(f))

with open("tests/data/linkedservice.json") as f:
    linkedservices_json_data = dict(load(f))


@pytest.fixture
def adf_pipeline():
    return Pipeline(
        name="pipeline",
        file_path="tests/data/pipeline.json",
        json_data=pipeline_json_data,
    )


@pytest.fixture
def adf_dataset():
    return Dataset(
        name="dataset",
        file_path="tests/data/dataset.json",
        json_data=dataset_json_data,
        linked_service_name="linkedservice",
    )


@pytest.fixture
def adf_linkedservice():
    return LinkedService(
        name="linkedservice",
        file_path="tests/data/linkedservice.json",
        json_data=linkedservices_json_data,
    )


@pytest.fixture
def adf_copy_activity():
    return [
        CopyActivity(
            name="Copy 1",
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
                    "parameters": {},
                }
            ],
            inputs_dataset_name="DS_REST",
            outputs_dataset_name="dataset",
        ),
        CopyActivity(
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
                    "parameters": {
                        "pFolder": {
                            "value": "@parameters('rawFolderPath')",
                            "type": "Expression",
                        }
                    },
                }
            ],
            inputs_dataset_name="DS_REST",
            outputs_dataset_name="dataset",
        ),
    ]
