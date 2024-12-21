from dataclasses import dataclass
from typing import Optional


@dataclass
class Pipeline:
    """Pipeline dataclass"""

    file_path: Optional[str]
    json_data: Optional[dict]
