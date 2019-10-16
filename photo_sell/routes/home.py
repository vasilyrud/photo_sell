import flask

from photo_sell.routes.login_state import decide_state
from photo_sell.routes.get_image import get_latest_images, download_thumbnail

home = flask.Blueprint('home', __name__, template_folder='photo_sell.templates')

@home.route('/')
def index():

    latest_images = get_latest_images()
    image_data = [
        download_thumbnail(drive_id) 
        for drive_id in latest_images
    ]

    return decide_state(images=image_data)
