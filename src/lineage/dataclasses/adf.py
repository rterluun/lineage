from dataclasses import dataclass
from typing import Optional


@dataclass
class Pipeline:
    """Pipeline dataclass"""

    file_path: Optional[str]
    json_data: Optional[dict]


@dataclass
class CopyActivity:
    """CopyActivity dataclass"""

    name: str
    inputs: list
    outputs: list
    inputs_dataset_name: str
    outputs_dataset_name: str


@dataclass
class Dataset:
    """Dataset dataclass"""

    name: Optional[str]
    file_path: Optional[str]
    json_data: Optional[dict]
    linked_service_name: Optional[str]
