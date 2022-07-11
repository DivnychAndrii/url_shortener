from typing import TYPE_CHECKING
import pytest

from source.managers import BaseManager

if TYPE_CHECKING:
    from tests.test_db import TestingSessionLocal


class TestBaseManager:

    @pytest.fixture
    def test_manager(self, db: 'TestingSessionLocal') -> BaseManager:
        yield BaseManager(db)

    def test_raise_error_no_model(self, test_manager: BaseManager):
        with pytest.raises(NotImplementedError):
            test_manager.get_model_object({})
