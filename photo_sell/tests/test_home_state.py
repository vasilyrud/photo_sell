import pytest

from photo_sell.models.image import Image

from photo_sell.routes.home import download_thumbnail, get_latest_images

def test_empty_images(client, const):
    rv = client.get('/')

    assert b'Sign in (with Google)' in rv.data

def test_logged_in_google(client, const):
    with client.session_transaction() as sess:
        sess['google_id'] = 'abc'

    rv = client.get('/')

    assert b'Connect with Stripe' in rv.data

def test_logged_in_stripe(client, const):
    with client.session_transaction() as sess:
        sess['google_id'] = 'abc'
        sess['stripe_id'] = 'def'

    rv = client.get('/')

    assert b'Add image to sell' in rv.data

def test_login_access(client, const):
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

def test_download_thumbnail(client, const):
    thumbnail_image_data = download_thumbnail(const['VALID_DRIVE_ID'])

    assert 'data:image/png;base64,' in thumbnail_image_data

def test_get_latest_images(client, const):
    cur_image = Image.add_drive_image(const['VALID_DRIVE_ID'], '1')
    cur_image = Image.add_drive_image('a' * 28, '2')

    latest_images = get_latest_images()

    assert len(latest_images) == 2
    assert const['VALID_DRIVE_ID'] in latest_images

def test_logout(client, const):
    with client.session_transaction() as sess:
        sess['google_id'] = 'abc'
        sess['stripe_id'] = 'def'

    rv = client.get('/logout', follow_redirects=True)

    with client.session_transaction() as sess:
        assert 'google_id' not in sess
        assert 'stripe_id' not in sess
