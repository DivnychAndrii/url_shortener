from typing import Union

from pydantic import BaseModel, AnyUrl, Field


class GenerateShortUrlRequestModel(BaseModel):
    target_url: AnyUrl = Field(
        description="Short version of provided url",
        example="https://www.google.com/test123123"
    )


class ShortUrlResponseModel(BaseModel):
    short_url: Union[AnyUrl, str] = Field(
        description="Short version of provided url",
        example="https://www.{host}//gncu34r"
    )
