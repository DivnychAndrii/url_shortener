from typing import Type

from source.models import ShortLinkClicksModel
from .base_manager import BaseManager


class ShortLinkClickManager(BaseManager):

    @property
    def model(self) -> Type[ShortLinkClicksModel]:
        return ShortLinkClicksModel

    def handle_clicks_count_object(self, user_id: int, url_mapping_id: int) -> model:
        attributes = {'user_id': user_id, 'url_mapping_id': url_mapping_id}
        short_link_clicks_obj = self.get_model_object(attributes)
        if not short_link_clicks_obj:
            short_link_clicks_obj = self.model(**attributes)
            self.session.add(short_link_clicks_obj)
            self.session.commit()

        return short_link_clicks_obj

    def update_clicks_count(self, user_id: int, url_mapping_id: int) -> None:
        db_object = self.handle_clicks_count_object(user_id=user_id, url_mapping_id=url_mapping_id)
        db_object.count += 1
        self.session.commit()
