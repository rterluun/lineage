from json import load

import pytest

from lineage.dataclasses.adf import CallDataset, CopyActivity, Dataset, Pipeline

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
        name="dataset",
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


@pytest.fixture
def call_datasets():
    return [
        CallDataset(
            copy_activity_name="Copy 1",
            datasets=[
                Dataset(
                    name="dataset",
                    file_path="tests/data/dataset.json",
                    json_data={
                        "name": "dataset",
                        "properties": {
                            "linkedServiceName": {
                                "referenceName": "linkedservice",
                                "type": "LinkedServiceReference",
                            },
                            "parameters": {"pFolder": {"type": "String"}},
                            "folder": {"name": "sample"},
                            "annotations": [],
                            "type": "Parquet",
                            "typeProperties": {
                                "location": {},
                                "compressionCodec": "snappy",
                            },
                            "schema": [],
                        },
                        "type": "Microsoft.DataFactory/factories/datasets",
                    },
                )
            ],
        ),
        CallDataset(
            copy_activity_name="Copy 2",
            datasets=[
                Dataset(
                    name="dataset",
                    file_path="tests/data/dataset.json",
                    json_data={
                        "name": "dataset",
                        "properties": {
                            "linkedServiceName": {
                                "referenceName": "linkedservice",
                                "type": "LinkedServiceReference",
                            },
                            "parameters": {"pFolder": {"type": "String"}},
                            "folder": {"name": "sample"},
                            "annotations": [],
                            "type": "Parquet",
                            "typeProperties": {
                                "location": {},
                                "compressionCodec": "snappy",
                            },
                            "schema": [],
                        },
                        "type": "Microsoft.DataFactory/factories/datasets",
                    },
                )
            ],
        ),
    ]
