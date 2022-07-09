from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .settings import test_settings

engine = create_engine(test_settings.SQLALCHEMY_TEST_DATABASE_URI)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestingSessionLocal = scoped_session(session_factory)


def get_test_db() -> Generator:
    test_db = None
    try:
        test_db = TestingSessionLocal()
        yield test_db
    finally:
        if test_db:
            test_db.close()
