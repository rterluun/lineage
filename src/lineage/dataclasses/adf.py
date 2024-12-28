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


@dataclass
class Dataset:
    """Dataset dataclass"""

    name: Optional[str]
    file_path: Optional[str]
    json_data: Optional[dict]


@dataclass
class CallDataset:
    """Dataset dataclass"""

    copy_activity_name: str
    datasets: list[Dataset]
