from os import environ as env
from typing import List

from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: str = env.get(
        "SQLALCHEMY_DATABASE_URI",
        "postgresql://user:pass@postgres:5432/db?sslmode=disable"
    )
    PORT: int = 5036
    RELOAD: bool = True
    ALLOWED_HOSTS: List[str] = ["*"]
    HOST: AnyUrl = env.get('HOST', f'http://0.0.0.0:{PORT}/')
    FILE_PATH_LENGTH: int = env.get('FILE_PATH_LENGTH', 7)


settings = Settings()
