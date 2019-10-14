import pytest

from photo_sell.routes.add_image_form import AddImageForm

def test_empty_db(client):

    form = AddImageForm()
    assert 1 == 1
