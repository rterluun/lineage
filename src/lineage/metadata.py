from logging import Logger, getLogger
from typing import List, Optional

from pymssql import Connection

import lineage.connectors.mssql as mssql
from lineage.dataclasses.metadata import Metadata, SearchConditionTable

LOGGER = getLogger(__name__)


class Dataset:
    def __init__(
        self,
        mssql_connection: Optional[Connection] = None,
        logger: Logger = LOGGER,
    ):
        self.mssql_connection = mssql_connection
        self.logger = logger
        self.result: List = []
        self.metadata: Optional[Metadata] = None

    @classmethod
    def from_mssql_connection(
        cls,
        server: str,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: str = "master",
        port: str = "1433",
        logger: Logger = LOGGER,
    ):
        return cls(
            mssql_connection=mssql.get_connection(
                server=server,
                user=user,
                password=password,
                database=database,
                port=port,
                logger=logger,
            ),
            logger=logger,
        )

    def execute(self, query: str):
        if self.mssql_connection:
            self.result = mssql.execute_query(
                connection=self.mssql_connection,
                query=query,
                logger=self.logger,
            )

            return self

    def set_metadata(self, search_condition_table: SearchConditionTable):

        try:
            self.metadata = Metadata(
                table_name=self.result[search_condition_table.row_index].get(
                    search_condition_table.column_name
                )
            )
        except IndexError:
            self.logger.error("Could not set metadata")

        return self
