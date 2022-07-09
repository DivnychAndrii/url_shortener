from typing import Generator

import pytest
from fastapi.testclient import TestClient

from source.database import get_db
from main import app
from source.models import Base

from .test_db import engine, get_test_db


@pytest.fixture
def db():
    yield get_test_db


@pytest.fixture(scope="session")
def prepare_db() -> Generator:
    """
    Create a fresh database before test cases.
    """
    # Create the tables.
    Base.metadata.create_all(engine)
    yield
    # Drop schemas after all test cases
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def client(prepare_db: None) -> Generator:
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as client:
        yield client

