from pydantic import BaseSettings

from os import environ as env


class TestSettings(BaseSettings):
    SQLALCHEMY_TEST_DATABASE_URI = (
        env.get("SQLALCHEMY_TEST_DATABASE_URI",
                "postgresql://user:pass@postgres:5432/db?sslmode=disable")
    )


test_settings = TestSettings()
