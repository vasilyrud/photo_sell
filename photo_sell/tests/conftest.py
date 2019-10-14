import pytest

import photo_sell

@pytest.fixture
def client():
    app = photo_sell.create_app(running_tests=True)
    client = app.test_client()

    return client
