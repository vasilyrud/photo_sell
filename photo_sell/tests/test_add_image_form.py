import pytest

from photo_sell.routes.add_image_form import AddImageForm

VALID_SUBURLS = [
    'drive.google.com/file/d/',
    'drive.google.com/open?id=',
]

VALID_DRIVE_ID = '0B4Edc2SFos9ANm1yU2Q0YVhEZ2c'

def test_parse_drive_url_valid(client):
    form = AddImageForm()

    valid_urls = [
        'https://' + VALID_SUBURLS[0] + VALID_DRIVE_ID + '/view?usp=sharing',
        VALID_SUBURLS[0] + VALID_DRIVE_ID + 'cd',
    ] + [
        suburl + VALID_DRIVE_ID for suburl in VALID_SUBURLS
    ]

    for valid_url in valid_urls:
        assert form._parse_drive_url(valid_url) == VALID_DRIVE_ID

def _assert_invalid_urls(form, invalid_urls):
    for invalid_url in invalid_urls:
        assert form._parse_drive_url(invalid_url) == None

def test_parse_drive_url_invalid_length(client):
    form = AddImageForm()

    invalid_urls = [
        VALID_SUBURLS[0] + VALID_DRIVE_ID[:-1],
        VALID_SUBURLS[0],
    ]

    _assert_invalid_urls(form, invalid_urls)

def test_parse_drive_url_invalid_prefix(client):
    form = AddImageForm()

    invalid_urls = [
        'drive.google.com' + VALID_DRIVE_ID,
        VALID_SUBURLS[0] + '/' + VALID_DRIVE_ID,
        VALID_DRIVE_ID,
    ]

    _assert_invalid_urls(form, invalid_urls)

def test_parse_drive_url_invalid_alnum(client):
    form = AddImageForm()

    invalid_urls = [
        VALID_SUBURLS[0] + '=' + VALID_DRIVE_ID[1:],
        VALID_SUBURLS[0] + VALID_DRIVE_ID[:-1] + '=',
    ]

    _assert_invalid_urls(form, invalid_urls)

def test_parse_drive_url_exists(client):
    form = AddImageForm()

    assert form._drive_image_exists(VALID_DRIVE_ID)

def test_parse_drive_url_does_not_exist(client):
    form = AddImageForm()

    assert not form._drive_image_exists(28 * 'a')
