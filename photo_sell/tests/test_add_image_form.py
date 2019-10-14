import os
import tempfile
import pytest

import photo_sell.config

@pytest.fixture
def client():
    app = photo_sell.create_app(running_tests=True)
    client = app.test_client()

    return client

def test_empty_db(client):
    rv = client.get('/')
    assert b'No images to see yet' in rv.data
