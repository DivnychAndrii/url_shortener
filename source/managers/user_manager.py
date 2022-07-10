from typing import Optional


from source.models import UserModel
from .base_manager import BaseManager


class UserManager(BaseManager):
    model = UserModel

    def get_user(self, public_identifier: str) -> Optional[model]:
        return self.session.query(self.model).filter_by(public_identifier=public_identifier).first()

    def get_or_create_user(self, public_identifier: str) -> model:
        user = self.get_user(public_identifier)
        if not user:
            user = self.model(public_identifier=public_identifier)
            self.session.add(user)
            self.session.commit()

        return user
