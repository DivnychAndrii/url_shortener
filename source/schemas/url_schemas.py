from typing import Union, Optional

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
    clicks_count: Optional[int] = Field(
        None,
        description="Total number of uses per user",
        example=2
    )
