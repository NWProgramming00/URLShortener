from pydantic import BaseModel
from datetime import datetime


class URLItem(BaseModel):
    url: str


class ShortenedURLResponse(BaseModel):
    short_url: str
    expiry_date: datetime


class ShortenedURLRequest(BaseModel):
    short_url: str
