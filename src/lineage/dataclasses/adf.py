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
