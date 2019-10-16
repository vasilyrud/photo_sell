import pytest

def test_empty_images(client):
    rv = client.get('/')

    assert b'Sign in (with Google)' in rv.data

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

def test_login_access(client):
    rv = client.get('/stripe_connect', follow_redirects=True)
    assert b'Sign in (with Google)' in rv.data

    rv = client.get('/stripe_auth', follow_redirects=True)
    assert b'Sign in (with Google)' in rv.data

    rv = client.get('/logout', follow_redirects=True)
    assert b'Sign in (with Google)' in rv.data

    with client.session_transaction() as sess:
        sess['google_id'] = 'abc'

    rv = client.get('/add_image', follow_redirects=True)
    assert b'Connect with Stripe' in rv.data
