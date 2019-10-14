import io
import flask
import base64
import requests
import imghdr

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

from photo_sell.models.db import db
from photo_sell.models.image import Image
from photo_sell.models.seller import Seller

from photo_sell.routes.login_state import decide_state
from photo_sell.routes.cache import cache

home = flask.Blueprint('home', __name__, template_folder='photo_sell.templates')

def _download_image(drive_id):

    service = build('drive', 'v3', developerKey=flask.current_app.config['GOOGLE_DRIVE_API_KEY'])
    request = service.files().get_media(fileId=drive_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

@cache.memoize(timeout=10)
def _get_latest_images():
    return [
        img.drive_id 
        for img in db.session.query(Image).order_by(Image.id.desc()).limit(5)
    ]

@cache.memoize(timeout=60*24)
def _download_thumbnail(drive_id):

    # TODO: Use Drive API to get thumbnail. If not possible,
    # download image and shrink manually.

    thumbnail_url = flask.current_app.config['GOOGLE_DRIVE_THUMBNAIL_URL'] + drive_id

    image_bytes = requests.get(thumbnail_url).content
    image_type  = imghdr.what(None, image_bytes)

    return 'data:image/' + image_type + ';base64, ' + base64.b64encode(image_bytes).decode('utf-8')

@home.route('/')
def index():

    latest_images = _get_latest_images()
    image_data = [
        _download_thumbnail(drive_id) 
        for drive_id in latest_images
    ]

    return decide_state(images=image_data)
