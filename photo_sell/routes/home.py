import flask

from photo_sell.models.common import db
from photo_sell.models.image import Image
from photo_sell.models.seller import Seller

home = flask.Blueprint('home', __name__, template_folder='photo_sell.templates')

@home.route('/')
def index():
    if 'google_id' in flask.session:
        if 'stripe_id' in flask.session:
            return flask.render_template('index/seller.html')
        else:
            return flask.render_template('index/connect.html')
    else:
        return flask.render_template('index/home.html')
