from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from source.database import get_db
from source.exceptions import NotFoundHTTPException
from source.schemas import (
    ShortUrlResponseModel,
    GenerateShortUrlRequestModel,
    UnprocessableEntity,
    NotFound
)
from source.managers import URLManager
from source.utils import generate_short_url_based_on_hash

router = APIRouter(tags=["URLs"])


@router.post(
    "/api/urls",
    summary="Generate short url endpoint",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": UnprocessableEntity}},
    response_model=ShortUrlResponseModel,
    description="The endpoint is intended to be used in order to generate short url out of a given one",
)
def generate(body: GenerateShortUrlRequestModel, db: Session = Depends(get_db)):
    url_manager = URLManager(db)

    url_mapping_obj = url_manager.get_url_object_by_filters(filters={'original_url': body.target_url})
    if not url_mapping_obj:
        url_mapping_obj = url_manager.create_short_url_hash(body.target_url)

    short_url = generate_short_url_based_on_hash(url_mapping_obj.hash_key)

    return ShortUrlResponseModel(short_url=short_url)


@router.get(
    "/api/{url_key}",
    summary="Redirect to the target endpoint by short key",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    responses={status.HTTP_404_NOT_FOUND: {"model": NotFound}},
    description="The endpoint is intended to redirect user to the target URL",
)
def redirect(url_key: str, db: Session = Depends(get_db)) -> RedirectResponse:
    url_manager = URLManager(db)

    url_mapping_obj = url_manager.get_url_object_by_filters(filters={'hash_key': url_key})
    if not url_mapping_obj:
        raise NotFoundHTTPException()

    return RedirectResponse(url_mapping_obj.original_url)


@router.get(
    "/home",
    summary="Render UI home page",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
def render_view(request: Request):
    templates = Jinja2Templates(directory="source/static")
    return templates.TemplateResponse("main.html", {"request": request})
