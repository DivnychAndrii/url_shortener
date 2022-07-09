from fastapi import FastAPI

from source.api import urls


def include_routers(app: FastAPI) -> None:
    app.include_router(urls.router)
