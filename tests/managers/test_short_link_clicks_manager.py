from typing import TYPE_CHECKING, List
from random import choice

from unittest.mock import MagicMock, patch
import pytest

from source.managers import ShortLinkClickManager
from source.models import ShortLinkClicksModel, UrlMappingsModel, UserModel

if TYPE_CHECKING:
    from tests.test_db import TestingSessionLocal


class TestShortLinkClicksManager:

    @pytest.fixture
    def test_manager(self, db: 'TestingSessionLocal') -> ShortLinkClickManager:
        yield ShortLinkClickManager(db)

    def test_get_url_object_by_filters(
            self,
            test_manager: ShortLinkClickManager,
            generate_short_link_clicks_objects: List[ShortLinkClicksModel]
    ) -> None:
        random_object = choice(generate_short_link_clicks_objects)
        test_filters = {'user_id': random_object.user_id,
                        'url_mapping_id': random_object.url_mapping_id}

        result = test_manager.get_model_object(filters=test_filters)

        assert result == random_object

    @patch.object(ShortLinkClickManager, 'handle_clicks_count_object')
    def test_update_clicks_count(self,
                                 handle_clicks_count_object_mock: MagicMock,
                                 test_manager: ShortLinkClickManager,
                                 generate_short_link_clicks_objects: List[
                                     ShortLinkClicksModel]) -> None:
        random_object = choice(generate_short_link_clicks_objects)
        initial_count = random_object.count

        handle_clicks_count_object_mock.return_value = random_object
        test_manager.update_clicks_count(random_object.user_id,
                                         random_object.url_mapping_id)
        result = test_manager.get_model_object(
            {'user_id': random_object.user_id,
             'url_mapping_id': random_object.url_mapping_id}, )

        assert result.count == initial_count + 1
        handle_clicks_count_object_mock.assert_called_once_with(
            user_id=random_object.user_id,
            url_mapping_id=random_object.url_mapping_id
        )

    @patch.object(ShortLinkClickManager, 'get_model_object', return_value=None)
    def test_handle_clicks_count_object_no_object(
            self,
            handle_clicks_count_object_mock: MagicMock,
            test_manager: ShortLinkClickManager,
            generate_url_mapping_objects:
            List[UrlMappingsModel],
            generate_users: List[UserModel]
    ) -> None:
        random_user = choice(generate_users)
        random_url = choice(generate_url_mapping_objects)

        result = test_manager.handle_clicks_count_object(random_user.id,
                                                         random_url.id)

        assert result.user_id == random_user.id
        assert result.url_mapping_id == random_url.id
        assert result.count == 0
        handle_clicks_count_object_mock.assert_called_once_with(
            {
                'user_id': random_user.id,
                'url_mapping_id': random_url.id
            }
        )

    @patch.object(ShortLinkClickManager, 'get_model_object')
    def test_handle_clicks_count_object_existing_object(
            self,
            handle_clicks_count_object_mock: MagicMock,
            test_manager: ShortLinkClickManager,
            generate_short_link_clicks_objects: List[ShortLinkClicksModel]
    ) -> None:
        random_object = choice(generate_short_link_clicks_objects)
        handle_clicks_count_object_mock.return_value = random_object

        result = test_manager.handle_clicks_count_object(random_object.user_id,
                                                         random_object.user_id)

        assert result == random_object
        handle_clicks_count_object_mock.assert_called_once_with(
            {
                'user_id': random_object.user_id,
                'url_mapping_id': random_object.url_mapping_id
            }
        )
