# test_db.py
import os
import pytest
from datetime import datetime
from db import DatabaseManager


@pytest.fixture
def database_manager():
    db_manager = DatabaseManager(host="test.db")
    yield db_manager
    db_manager.close()
    os.remove("test.db")


def test_add_url(database_manager):
    url_id = database_manager.add_url("https://example.com", datetime.now())
    assert isinstance(url_id, int)


def test_select_url(database_manager):
    url_id = database_manager.add_url("https://example.com", datetime.now())
    selected_url = database_manager.select_url(url_id)
    assert selected_url == "https://example.com"
