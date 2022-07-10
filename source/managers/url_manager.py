from typing import Optional, Dict, Any, Union

from pydantic import AnyUrl

from source.models import UrlMappingsModel
from source.utils import generate_random_hash
from .base_manager import BaseManager


class URLManager(BaseManager):
    model = UrlMappingsModel

    def get_url_object_by_filters(
            self,
            filters: Dict[str, Any]
    ) -> Optional[UrlMappingsModel]:
        return self.session.query(self.model).filter_by(**filters).first()

    def get_or_create_short_url_hash(self, url: Union[AnyUrl, str]) -> UrlMappingsModel:
        db_object = self.get_url_object_by_filters({'original_url': url})

        if not db_object:
            random_hash = generate_random_hash(target_str=url)
            db_object = self.model(
                original_url=url,
                hash_key=random_hash
            )
            self.session.add(db_object)
            self.session.commit()

        return db_object

