from dataclasses import dataclass


@dataclass
class SearchConditionTable:
    """SearchConditionTable dataclass"""

    column_name: str
    row_index: int


@dataclass
class Metadata:
    """Metadata dataclass"""

    table_name: str
