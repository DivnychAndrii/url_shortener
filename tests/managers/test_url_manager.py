import uuid
from random import choice
from typing import TYPE_CHECKING, List

import pytest
from unittest.mock import MagicMock, patch

from source.models import UrlMappingsModel
from source.managers import URLManager


if TYPE_CHECKING:
    from tests.test_db import TestingSessionLocal


class TestUrlManager:

    @pytest.fixture
    def test_manager(self,  db: 'TestingSessionLocal') -> URLManager:
        yield URLManager(db)

    @pytest.fixture
    def generate_url_mapping_objects(self, db: 'TestingSessionLocal') -> List[UrlMappingsModel]:
        model_objects = []
        for _ in range(3):
            random_uuid = str(uuid.uuid4())

            new_mapping_object = UrlMappingsModel(
                original_url=f'http://www.test.com/{random_uuid}',
                hash_key=random_uuid
            )
            db.add(new_mapping_object)
            model_objects.append(new_mapping_object)
        db.commit()

        yield model_objects

    @pytest.mark.parametrize('key', ['id', 'original_url', 'hash_key'])
    def test_get_url_object_by_filters(self,
                                       test_manager: URLManager,
                                       generate_url_mapping_objects: List[UrlMappingsModel],
                                       key: str) -> None:
        random_object = choice(generate_url_mapping_objects)
        test_filters = {key: getattr(random_object, key)}

        result = test_manager.get_url_object_by_filters(filters=test_filters)

        assert result == random_object

    @patch('source.managers.url_manager.generate_random_hash')
    def test_create_short_url_hash(self,
                                   generate_random_hash_mock: MagicMock,
                                   test_manager: URLManager) -> None:
        random_uuid = str(uuid.uuid4())
        test_url = f'http://www.test.com/{random_uuid}'

        generate_random_hash_mock.return_value = random_uuid

        result = test_manager.create_short_url_hash(url=test_url)

        assert getattr(result, 'original_url') == test_url
        assert getattr(result, 'hash_key') == random_uuid
