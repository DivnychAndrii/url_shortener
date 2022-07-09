from fastapi import status
from pydantic import BaseModel


class Error(BaseModel):
    detail: str
    status: int
    title: str
    type: str


class UnprocessableEntity(Error):
    class Config:
        schema_extra = {
            "example": {
                "detail": "{Description error}",
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "title": "Unprocessable entity",
                "type": "about:blank",
            }
        }