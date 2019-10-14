import pytest

def test_empty_images(client):
    rv = client.get('/')

    assert b'No images to see yet' in rv.data

def test_logged_in_google(client):
    with client.session_transaction() as sess:
        sess['google_id'] = 'abc'

    rv = client.get('/')

    assert b'Connect with Stripe' in rv.data

def test_logged_in_stripe(client):
    with client.session_transaction() as sess:
        sess['google_id'] = 'abc'
        sess['stripe_id'] = 'def'

    rv = client.get('/')

    assert b'Add image to sell' in rv.data
