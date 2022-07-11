import os

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
        proxy_headers=True,
        forwarded_allow_ips='*',
        docs_url='/docs'
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    include_routers(app)

    project_dir = os.path.dirname(__file__)
    app.mount("/static",
              StaticFiles(directory=os.path.join(project_dir, "static/")),
              name="static")

    return app
