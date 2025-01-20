from dataclasses import dataclass
from typing import Optional

from lineage.dataclasses.metadata import Metadata


@dataclass
class Pipeline:
    """Pipeline dataclass"""

    name: Optional[str]
    file_path: Optional[str]
    json_data: Optional[dict]
    metadata: Optional[Metadata]


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
    metadata: Optional[Metadata]


@dataclass
class LinkedService:
    """LinkedService dataclass"""

    name: Optional[str]
    file_path: Optional[str]
    json_data: Optional[dict]
    metadata: Optional[Metadata]


@dataclass
class PipelineReference:
    """PipelineReference dataclass"""

    name: str
    pipeline: str


@dataclass
class PipelineParameter:
    """PipelineParameter dataclass"""

    name: str
    type: Optional[str]
    default_value: Optional[str]
    current_value: Optional[str]
