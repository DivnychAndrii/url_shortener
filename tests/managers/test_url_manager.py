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
    def test_manager(self, db: 'TestingSessionLocal') -> URLManager:
        yield URLManager(db)

    @pytest.mark.parametrize('key', ['id', 'original_url', 'hash_key'])
    def test_get_url_object_by_filters(self,
                                       test_manager: URLManager,
                                       generate_url_mapping_objects: List[UrlMappingsModel],
                                       key: str) -> None:
        random_object = choice(generate_url_mapping_objects)
        test_filters = {key: getattr(random_object, key)}

        result = test_manager.get_model_object(filters=test_filters)

        assert result == random_object

    @patch.object(URLManager, 'get_model_object', return_value=None)
    @patch('source.managers.url_manager.generate_random_hash')
    def test_create_short_url_hash_no_object_found(self,
                                                   generate_random_hash_mock: MagicMock,
                                                   get_model_object_mock: MagicMock,
                                                   test_manager: URLManager) -> None:
        random_uuid = str(uuid.uuid4())
        test_url = f'https://www.test.com/{random_uuid}'
        generate_random_hash_mock.return_value = random_uuid

        result = test_manager.get_or_create_short_url_hash(url=test_url)

        assert getattr(result, 'original_url') == test_url
        assert getattr(result, 'hash_key') == random_uuid
        generate_random_hash_mock.assert_called_once_with(target_str=test_url)
        get_model_object_mock.assert_called_once_with({'original_url': test_url})

    @patch.object(URLManager, 'get_model_object')
    @patch('source.managers.url_manager.generate_random_hash')
    def test_create_short_url_hash_object_already_exist(self,
                                                        generate_random_hash_mock: MagicMock,
                                                        get_model_object_mock: MagicMock,
                                                        generate_url_mapping_objects: List[UrlMappingsModel],
                                                        test_manager: URLManager) -> None:
        target_object = generate_url_mapping_objects[0]
        get_model_object_mock.return_value = target_object

        result = test_manager.get_or_create_short_url_hash(url=target_object.original_url)

        assert result == target_object
        get_model_object_mock.assert_called_once_with({'original_url': target_object.original_url})
        generate_random_hash_mock.assert_not_called()
