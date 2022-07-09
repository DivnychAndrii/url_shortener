from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from source.database import get_db
from source.schemas import (
    ShortUrlResponseModel,
    GenerateShortUrlRequestModel,
    UnprocessableEntity,
)
from source.managers import URLManager
from source.models import UrlMappingsModel
router = APIRouter(prefix="/urls", tags=["URLs"])


@router.post(
    "",
    summary="Generate short url endpoint",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": UnprocessableEntity}},
    response_model=ShortUrlResponseModel,
    description="The endpoint is intended to be used in order to generate short url out of a given one",
)
def generate(body: GenerateShortUrlRequestModel, db: Session = Depends(get_db)):
    url_manager = URLManager(db)
    filters = {'original_url': body.target_url}

    url_mapping = url_manager.get_url_object_by_filters(filters=filters)
    if not url_mapping:
        url_mapping = url_manager.generate_short_url(body.target_url)

    return ShortUrlResponseModel(short_url=url_mapping.short_url)
