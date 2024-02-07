import pytest
from fastapi.testclient import TestClient
from settings import settings
settings.database.host = "test.db"
from main import app


@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app)


def test_encode_url(test_app):
    response = test_app.post("/encode", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    assert "expiry_date" in data
    assert isinstance(data["short_url"], str)
    assert data["expiry_date"] is not None


def test_decode_url(test_app):
    response = test_app.post("/encode", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    short_url = data["short_url"]

    decode_response = test_app.post("/decode", json={"short_url": short_url})
    assert decode_response.status_code == 200
    decode_data = decode_response.json()
    assert "url" in decode_data
    assert decode_data["url"] == "https://example.com"


def test_invalid_encode_request(test_app):
    response = test_app.post("/encode", json={"invalid_key": "https://example.com"})
    assert response.status_code == 422


def test_invalid_decode_request(test_app):
    response = test_app.post("/decode", json={"invalid_key": "invalid_url"})
    assert response.status_code == 422


def test_decode_nonexistent_url(test_app):
    response = test_app.post("/decode", json={"short_url": "http://short.est/invalid_code"})
    assert response.status_code == 404
