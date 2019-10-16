import pytest

from photo_sell.models.db import db
from photo_sell.models.image import Image
from photo_sell.models.seller import Seller

from photo_sell.routes.add_image_form import AddImageForm

def test_parse_drive_url_valid(client, const):
    form = AddImageForm()

    valid_urls = [
        'https://' + const['VALID_SUBURLS'][0] + const['VALID_DRIVE_ID'] + '/view?usp=sharing',
        const['VALID_SUBURLS'][0] + const['VALID_DRIVE_ID'] + 'cd',
    ] + [
        suburl + const['VALID_DRIVE_ID'] for suburl in const['VALID_SUBURLS']
    ]

    for valid_url in valid_urls:
        assert form._parse_drive_url(valid_url) == const['VALID_DRIVE_ID']

def _assert_invalid_urls(form, invalid_urls):
    for invalid_url in invalid_urls:
        assert form._parse_drive_url(invalid_url) == None

def test_parse_drive_url_invalid_length(client, const):
    form = AddImageForm()

    invalid_urls = [
        const['VALID_SUBURLS'][0] + const['VALID_DRIVE_ID'][:-1],
        const['VALID_SUBURLS'][0],
    ]

    _assert_invalid_urls(form, invalid_urls)

def test_parse_drive_url_invalid_prefix(client, const):
    form = AddImageForm()

    invalid_urls = [
        'drive.google.com' + const['VALID_DRIVE_ID'],
        const['VALID_SUBURLS'][0] + '/' + const['VALID_DRIVE_ID'],
        const['VALID_DRIVE_ID'],
    ]

    _assert_invalid_urls(form, invalid_urls)

def test_parse_drive_url_invalid_alnum(client, const):
    form = AddImageForm()

    invalid_urls = [
        const['VALID_SUBURLS'][0] + '=' + const['VALID_DRIVE_ID'][1:],
        const['VALID_SUBURLS'][0] + const['VALID_DRIVE_ID'][:-1] + '=',
    ]

    _assert_invalid_urls(form, invalid_urls)

def test_parse_drive_url_exists(client, const):
    form = AddImageForm()

    assert form._drive_image_exists(const['VALID_DRIVE_ID'])

def test_parse_drive_url_does_not_exist(client, const):
    form = AddImageForm()

    assert not form._drive_image_exists(28 * 'a')

def _create_seller(client, google_id, stripe_id):
    seller = Seller.add_google_id(google_id)
    seller = Seller.add_stripe_id(stripe_id, seller.id)

    with client.session_transaction() as sess:
        sess['google_id'] = seller.google_id
        sess['stripe_id'] = seller.stripe_id
        sess['seller_id'] = seller.id

    return seller

def test_form_submit(client, const):
    _create_seller(client, 'abc', 'def')

    rv = client.get('/add_image')
    assert b'<form' in rv.data and b'Add Image' in rv.data

    with client.session_transaction() as sess:
        response = client.post('/add_image', data={
            'drive_url': const['VALID_SUBURLS'][0] + const['VALID_DRIVE_ID']
        }, follow_redirects=True)

    assert b'Add image to sell' in response.data

def test_form_submit_error(client, const):
    _create_seller(client, 'abc', 'def')

    rv = client.get('/add_image')
    assert b'<form' in rv.data and b'Add Image' in rv.data

    with client.session_transaction() as sess:
        response = client.post('/add_image', data={
            'drive_url': 'not valid'
        }, follow_redirects=True)

    assert b'Invalid Google Drive URL provided' in response.data
