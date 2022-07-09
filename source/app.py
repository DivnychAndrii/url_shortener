from fastapi import FastAPI
from source import settings


def create_app() -> FastAPI:

    app = FastAPI(
        title='Url shortener',
        description='Url shortener',
        debug=settings.DEBUG,
        docs_url='/docs'
    )

    return app
