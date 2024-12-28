from json import load

import pytest

from lineage.dataclasses.adf import CopyActivity, Dataset, Pipeline

with open("tests/data/pipeline.json") as f:
    pipeline_json_data = dict(load(f))

with open("tests/data/dataset.json") as f:
    dataset_json_data = dict(load(f))


@pytest.fixture
def adf_pipeline():
    return Pipeline(
        file_path="tests/data/pipeline.json",
        json_data=pipeline_json_data,
    )


@pytest.fixture
def adf_dataset():
    return Dataset(
        file_path="tests/data/dataset.json",
        json_data=dataset_json_data,
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
        ),
    ]
