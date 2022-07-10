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
        return self.session.query(UrlMappingsModel).filter_by(**filters).first()

    def create_short_url_hash(self, url: Union[AnyUrl, str]) -> UrlMappingsModel:
        random_hash = generate_random_hash(target_str=url)
        new_mapping_object = self.model(
            original_url=url,
            hash_key=random_hash
        )
        self.session.add(new_mapping_object)
        self.session.commit()

        return new_mapping_object

