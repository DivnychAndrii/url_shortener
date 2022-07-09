from typing import TYPE_CHECKING

from fastapi import FastAPI
from source.settings import settings

if TYPE_CHECKING:
    from source.settings import Settings


def create_app(config: 'Settings' = settings) -> FastAPI:

    app = FastAPI(
        title='Url shortener',
        description='Url shortener',
        debug=config.DEBUG,
        docs_url='/docs'
    )

    return app
