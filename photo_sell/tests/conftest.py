import pytest

import photo_sell

@pytest.fixture
def const():
    return {
        'VALID_DRIVE_ID': '0B4Edc2SFos9ANm1yU2Q0YVhEZ2c',
        'VALID_SUBURLS': [
            'drive.google.com/file/d/',
            'drive.google.com/open?id=',
        ],
    }

@pytest.fixture
def client():
    app = photo_sell.create_app(running_tests=True)
    client = app.test_client()

    return client
