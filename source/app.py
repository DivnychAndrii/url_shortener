from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware


from source.settings import settings
from source.routers import include_routers

if TYPE_CHECKING:
    from source.settings import Settings


def create_app(config: 'Settings' = settings) -> FastAPI:

    app = FastAPI(
        title='Url shortener',
        description='Url shortener',
        debug=config.DEBUG,
        docs_url='/docs'
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    include_routers(app)
    app.mount("/static", StaticFiles(directory="source/static"), name="static")

    return app
