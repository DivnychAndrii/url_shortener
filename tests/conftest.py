from typing import Generator, TYPE_CHECKING, List
from random import randint
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from source.database import get_db
from main import app
from source.models import (
    Base,
    UserModel,
    UrlMappingsModel,
    ShortLinkClicksModel,
)

from .test_db import engine, get_test_db

if TYPE_CHECKING:
    from tests.test_db import TestingSessionLocal

db = pytest.fixture(get_test_db)


@pytest.fixture(scope="session", autouse=True)
def prepare_db() -> Generator:
    """
    Create a fresh database before test cases.
    """
    # Create the tables.
    Base.metadata.create_all(bind=engine)
    yield
    # Drop schemas after all test cases
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def client(prepare_db: None) -> Generator:
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture
def generate_users(db: 'TestingSessionLocal') -> List[UserModel]:
    model_objects = []
    for _ in range(3):
        random_identification = str(randint(100, 10000))

        new_user = UserModel(public_identifier=random_identification)
        db.add(new_user)
        model_objects.append(new_user)

    db.commit()
    return model_objects


@pytest.fixture
def generate_url_mapping_objects(
        db: 'TestingSessionLocal'
) -> List[UrlMappingsModel]:
    model_objects = []
    for _ in range(3):
        random_uuid = str(uuid4())

        new_mapping_object = UrlMappingsModel(
            original_url=f'https://www.test.com/{random_uuid}',
            hash_key=random_uuid
        )
        db.add(new_mapping_object)
        model_objects.append(new_mapping_object)
    db.commit()

    yield model_objects


@pytest.fixture
def generate_short_link_clicks_objects(
        generate_users,
        generate_url_mapping_objects,
        db: 'TestingSessionLocal'
) -> List[ShortLinkClicksModel]:
    model_objects = []
    for user, url in zip(generate_users, generate_url_mapping_objects):
        new_object = ShortLinkClicksModel(
            user_id=user.id,
            url_mapping_id=url.id,
            count=randint(0, 10)
        )
        db.add(new_object)
        model_objects.append(new_object)
    db.commit()

    yield model_objects
