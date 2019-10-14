import flask

from photo_sell.models.db import db
from photo_sell.models.image import Image
from photo_sell.models.seller import Seller

from photo_sell.routes.login_state import decide_state

home = flask.Blueprint('home', __name__, template_folder='photo_sell.templates')

@home.route('/')
def index():
    return decide_state()
