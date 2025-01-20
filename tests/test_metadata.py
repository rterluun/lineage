import unittest.mock as mock
from unittest.mock import patch

import lineage.dataclasses.metadata as dataclasses

# import Metadata, SearchConditionTable
from lineage.metadata import Metadata


@patch("lineage.connectors.mssql.connect")
def test_metadata_from_mssql_connection(mock_pymssql_connect):

    mock_conn = mock.MagicMock()
    mock_pymssql_connect.return_value = mock_conn

    Metadata.from_mssql_connection(
        server="server",
        user="admin",
        password="admin",
        database="master",
        port="1433",
    )

    mock_pymssql_connect.assert_called_once_with(
        server="server",
        user="admin",
        password="admin",
        database="master",
        port="1433",
    )


@patch("lineage.connectors.mssql.Connection")
def test_metadata_execute(mock_pymssql_connection):

    Metadata(
        mssql_connection=mock_pymssql_connection,
    ).execute(query="SELECT table_name FROM test_table")

    mock_pymssql_connection.cursor.assert_called_once_with(as_dict=True)


@patch("lineage.connectors.mssql.Connection")
def test_metadata_set_metadata(mock_pymssql_connection):

    metadata = Metadata(
        mssql_connection=mock_pymssql_connection,
    )

    metadata.result = [
        {"col0": "foo", "col1": "bar"},  # row_index=0
        {"col0": "bar", "col1": "foo"},  # row_index=1
    ]

    assert metadata.set_metadata(
        search_condition_table=dataclasses.SearchConditionTable(
            row_index=1,
            column_name="col1",
        )
    ).metadata == dataclasses.Metadata(table_name="foo")
