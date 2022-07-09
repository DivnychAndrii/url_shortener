"""
Managers module is intended to work with DB entities and realize the business logic
"""
from typing import List, Optional, Dict, Any, Union

from pydantic import AnyUrl

from source.models import UrlMappingsModel
from source.utils import generate_random_hash
from .base_manager import BaseManager


class URLManager(BaseManager):
    model = UrlMappingsModel

    def get_url_object_by_filters(
            self,
            filters: Dict[str, Any],
            method: str = 'first'
    ) -> Union[List[Optional[UrlMappingsModel]], Optional[UrlMappingsModel]]:
        return getattr(self.session.query(UrlMappingsModel).filter_by(**filters), method)()

    def generate_short_url(self, url: AnyUrl) -> UrlMappingsModel:
        random_hash = generate_random_hash(target_str=url)
        new_mapping_object = self.model(
            original_url=url,
            short_url=random_hash
        )
        self.session.add(new_mapping_object)
        self.session.commit()

        return new_mapping_object

