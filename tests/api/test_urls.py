from random import choice
import pytest
from unittest.mock import patch, MagicMock

from typing import TYPE_CHECKING, List
from fastapi import status

from source.managers import ShortLinkClickManager, UserManager, URLManager
from source.models import UserModel, ShortLinkClicksModel, UrlMappingsModel

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


class TestGenerateUrl:
    endpoint = '/api/urls'

    def test_generate_endpoint_integration(self, client: 'TestClient'):
        test_valid_body = {
            'target_url': 'https://www.google.com'
        }
        response = client.post(self.endpoint, json=test_valid_body)
        assert response.status_code == status.HTTP_200_OK
        assert all(item in response.json() for item in ['short_url', 'clicks_count'])

    @patch('source.api.urls.generate_short_url_based_on_hash')
    @patch.object(ShortLinkClickManager, 'handle_clicks_count_object')
    @patch.object(UserManager, 'get_or_create_user')
    @patch.object(URLManager, 'get_or_create_short_url_hash')
    def test_generate_endpoint_schema_success(self,
                                              get_or_create_short_url_hash_mock: MagicMock,
                                              get_or_create_user_mock: MagicMock,
                                              handle_clicks_count_object_mock: MagicMock,
                                              generate_short_url_based_on_hash_mock: MagicMock,
                                              generate_users: List[UserModel],
                                              generate_url_mapping_objects: List[UrlMappingsModel],
                                              generate_short_link_clicks_objects: List[ShortLinkClicksModel],
                                              client: 'TestClient') -> None:
        test_valid_body = {
            'target_url': 'https://www.google.com'
        }
        test_short_link = 'www.test.com/1'
        random_short_link_obj = choice(generate_short_link_clicks_objects)

        get_or_create_short_url_hash_mock.return_value = choice(generate_url_mapping_objects)
        get_or_create_user_mock.return_value = choice(get_or_create_user_mock)
        handle_clicks_count_object_mock.return_value = random_short_link_obj
        generate_short_url_based_on_hash_mock.return_value = test_short_link

        response = client.post(self.endpoint, json=test_valid_body)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'short_url': test_short_link, 'clicks_count': random_short_link_obj.count}
        get_or_create_short_url_hash_mock.assert_called_once()
        get_or_create_user_mock.assert_called_once()
        handle_clicks_count_object_mock.assert_called_once()
        generate_short_url_based_on_hash_mock.assert_called_once()

    @pytest.mark.parametrize('key', ['', 'target_urlsc'])
    def test_generate_endpoint_schema_fail(self, client: 'TestClient', key: str) -> None:
        test_invalid_body = {
            key: 'https://www.google.com'
        }
        response = client.post(self.endpoint, json=test_invalid_body)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestRedirectUrl:
    endpoint = '/api/{url_key}'

    @patch.object(ShortLinkClickManager, 'update_clicks_count')
    @patch.object(UserManager, 'get_or_create_user')
    @patch.object(URLManager, 'get_model_object')
    def test_redirect_endpoint_schema_success(self,
                                              get_model_object_mock: MagicMock,
                                              get_or_create_user_mock: MagicMock,
                                              update_clicks_count_mock: MagicMock,
                                              generate_users: List[UserModel],
                                              generate_url_mapping_objects: List[UrlMappingsModel],
                                              generate_short_link_clicks_objects: List[ShortLinkClicksModel],
                                              client: 'TestClient') -> None:
        valid_url_object = choice(generate_url_mapping_objects)

        get_model_object_mock.return_value = valid_url_object
        get_or_create_user_mock.return_value = choice(get_or_create_user_mock)

        response = client.get(self.endpoint.format(url_key=valid_url_object.hash_key))

        assert next(iter(response.history)).status_code == status.HTTP_307_TEMPORARY_REDIRECT
        get_model_object_mock.assert_called_once()
        get_or_create_user_mock.assert_called_once()
        update_clicks_count_mock.assert_called_once()

    @patch.object(URLManager, 'get_model_object', return_value=None)
    def test_redirect_endpoint_not_found(self,
                                         get_model_object_mock: MagicMock,
                                         client: 'TestClient') -> None:
        response = client.get(self.endpoint.format(url_key='123'))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        get_model_object_mock.assert_called_once()

    def test_redirect_schema_fail(self, client: 'TestClient') -> None:
        response = client.get('/api/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestRenderView:
    endpoint = '/home'

    def test_render_view_success(self, client: 'TestClient'):

        response = client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.template.name == 'main.html'
