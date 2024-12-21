from json import load

import pytest

from lineage.dataclasses.adf import CopyActivity, Pipeline

with open("tests/data/pipeline.json") as f:
    json_data = dict(load(f))


@pytest.fixture
def adf_pipeline():
    return Pipeline(
        file_path="tests/data/pipeline.json",
        json_data=json_data,
    )


@pytest.fixture
def adf_copy_activity():
    return [
        [
            CopyActivity(
                name="Copy",
                inputs=[
                    {
                        "referenceName": "DS_REST",
                        "type": "DatasetReference",
                        "parameters": {},
                    }
                ],
                outputs=[
                    {
                        "referenceName": "DS_BlobFS",
                        "type": "DatasetReference",
                        "parameters": {
                            "pFolder": {
                                "value": "@parameters('rawFolderPath')",
                                "type": "Expression",
                            }
                        },
                    }
                ],
            )
        ]
    ]
