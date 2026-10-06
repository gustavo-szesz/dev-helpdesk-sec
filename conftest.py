import pytest

from app.db import connect,  create_table
from app.seed import seed

@pytest.fixture
def con():
    connection = connect(":memory:")
    create_table(connection)
    yield connection
    connection.close()

@pytest.fixture
def ids(con):
    return seed(con)