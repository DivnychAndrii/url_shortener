from typing import Type

from source.models import UserModel
from .base_manager import BaseManager


class UserManager(BaseManager):

    @property
    def model(self) -> Type[UserModel]:
        return UserModel

    def get_or_create_user(self, public_identifier: str) -> model:
        user = self.get_model_object({'public_identifier': public_identifier})
        if not user:
            user = self.model(public_identifier=public_identifier)
            self.session.add(user)
            self.session.commit()

        return user
