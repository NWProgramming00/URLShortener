from fastapi import FastAPI, HTTPException, Depends, status

from datetime import datetime, UTC

from settings import settings
from schemas import (URLItem, ShortenedURLResponse, ShortenedURLRequest)
from algorithm import HashingAlgorithm
from db import get_database_manager, DatabaseManager

app = FastAPI()
algorithm = HashingAlgorithm(salt=settings.algorithm_salt, min_length=settings.algorithm_min_length)


@app.post("/encode", response_model=ShortenedURLResponse)
async def encode(url_item: URLItem, db: DatabaseManager = Depends(get_database_manager)):
    url = url_item.url
    if not isinstance(url, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request.")

    expiry_date = datetime.now(UTC)
    url_db_id = db.add_url(url=url, expiry_date=expiry_date)
    short_code = algorithm.encode(number=url_db_id)
    short_url = f"{settings.host}{short_code}"
    return ShortenedURLResponse(short_url=short_url, expiry_date=expiry_date)


@app.post("/decode", response_model=URLItem)
async def decode(url: ShortenedURLRequest, db: DatabaseManager = Depends(get_database_manager)):
    short_url = url.short_url
    short_code = short_url.replace(settings.host, "")

    url_db_id = algorithm.decode(text=short_code)
    if not isinstance(url_db_id, int):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    url = db.select_url(id=url_db_id)
    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    return URLItem(url=url)
