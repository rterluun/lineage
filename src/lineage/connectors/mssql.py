from logging import Logger, getLogger
from typing import List, Optional

from pymssql import Connection, connect
from pymssql.exceptions import OperationalError, ProgrammingError

LOGGER = getLogger(__name__)


def get_connection(
    server: str,
    user: Optional[str] = None,
    password: Optional[str] = None,
    database: str = "master",
    port: str = "1433",
    logger: Logger = LOGGER,
) -> Optional[Connection]:

    connection = None

    try:
        connection = connect(
            server=server,
            user=user,
            password=password,
            database=database,
            port=port,
        )

    except OperationalError as e:
        logger.error(f"Error connecting to MSSQL: {e}")

    return connection


def execute_query(
    connection: Connection,
    query: str,
    logger: Logger = LOGGER,
) -> List:
    result: List = []

    with connection.cursor(as_dict=True) as cursor:
        try:
            cursor.execute(query)
            result = cursor.fetchall()

        except (ProgrammingError, OperationalError) as e:
            logger.error(f"Error executing query: {e}")

    return result
