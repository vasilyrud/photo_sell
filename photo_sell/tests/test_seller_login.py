import pytest

def test_google_login(client, const):
    rv = client.get('/google_login')

    assert b'https://accounts.google.com/o/oauth2/v2/auth' in rv.data

def test_stripe_connect(client, const):
    with client.session_transaction() as sess:
        sess['google_id'] = 'abc'

    rv = client.get('/stripe_connect')

    assert b'https://connect.stripe.com/oauth/authorize' in rv.data
