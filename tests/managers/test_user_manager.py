from typing import TYPE_CHECKING, List
from random import randint, choice

from unittest.mock import MagicMock, patch
import pytest

from source.managers import UserManager
from source.models import UserModel

if TYPE_CHECKING:
    from tests.test_db import TestingSessionLocal


class TestUserManager:

    @pytest.fixture
    def test_manager(self, db: 'TestingSessionLocal') -> UserManager:
        yield UserManager(db)

    @pytest.mark.parametrize('key', [
        column.key for column in UserModel.__table__.columns
    ])
    def test_users_by_filters(self,
                              test_manager: UserManager,
                              generate_users: List[UserModel],
                              key: str) -> None:
        random_object = choice(generate_users)
        test_filters = {key: getattr(random_object, key)}

        result = test_manager.get_model_object(filters=test_filters)

        assert result == random_object

    @patch.object(UserManager, 'get_model_object')
    def test_get_or_create_user_user_exists(self,
                                            get_model_object_mock: MagicMock,
                                            generate_users: List[UserModel],
                                            test_manager: UserManager) -> None:
        existing_user = choice(generate_users)
        get_model_object_mock.return_value = existing_user

        result = test_manager.get_or_create_user(
            existing_user.public_identifier
        )

        assert result == existing_user
        get_model_object_mock.assert_called_once_with(
            {'public_identifier': existing_user.public_identifier}
        )

    @patch.object(UserManager, 'get_model_object', return_value=None)
    def test_get_or_create_user_no_existing_users(
            self,
            get_model_object_mock: MagicMock,
            generate_users: List[UserModel],
            test_manager: UserManager
    ) -> None:
        test_identifier = str(randint(1000, 10000))
        result = test_manager.get_or_create_user(test_identifier)

        assert result.public_identifier == test_identifier
        assert isinstance(result, UserModel)
        get_model_object_mock.assert_called_once_with(
            {'public_identifier': test_identifier}
        )
