import flask

from photo_sell.models.common import db
from photo_sell.models.image import Image
from photo_sell.models.seller import Seller

from photo_sell.routes.oauth import authorize_url, get_user_info, authenticate

seller = flask.Blueprint('seller', __name__, template_folder='photo_sell.templates')

def get_seller(google_id):

    if not db.session.query(db.exists().where(
        Seller.google_id == google_id
    )).scalar():
        print('Creating user', google_id)
        db.session.add(Seller(google_id=google_id))
        db.session.commit()

    return db.session.query(Seller).filter(
        Seller.google_id == google_id
    ).first()

def add_stripe_id(stripe_id):

    cur_seller = db.session.query(Seller).filter(
        Seller.id == flask.session['seller_id']
    ).first()

    cur_seller.stripe_id = stripe_id
    db.session.commit()

    return cur_seller

@seller.route('/google_login')
def google_login():

    auth_url = authorize_url(
        'google',
        flask.current_app.config['GOOGLE_AUTH_URL'],
        'openid',
        flask.current_app.config['GOOGLE_CLIENT_ID']
    )

    return flask.redirect(auth_url)

@seller.route('/google_auth')
def google_auth():

    user_info = get_user_info(
        'google',
        flask.current_app.config['GOOGLE_INFO_URL'],
        flask.current_app.config['GOOGLE_CLIENT_SECRET'],
        flask.current_app.config['GOOGLE_CLIENT_ID']
    )

    if user_info is None:
        return flask.redirect('/')

    id_token_data = authenticate(
        flask.current_app.config['GOOGLE_LOGIN_URL'],
        user_info
    )

    google_id = id_token_data['sub']

    cur_seller = get_seller(google_id)
    flask.session['seller_id'] = cur_seller.id
    flask.session['google_id'] = google_id

    if cur_seller.stripe_id is not None:
        flask.session['stripe_id'] = cur_seller.stripe_id

    return flask.redirect('/')

@seller.route('/stripe_connect')
def stripe_connect():

    auth_url = authorize_url(
        'stripe',
        flask.current_app.config['STRIPE_AUTH_URL'],
        'read_write',
        flask.current_app.config['STRIPE_CLIENT_ID']
    )

    return flask.redirect(auth_url)

@seller.route('/stripe_auth')
def stripe_auth():

    user_info = get_user_info(
        'stripe',
        flask.current_app.config['STRIPE_INFO_URL'],
        flask.current_app.config['STRIPE_CLIENT_SECRET'],
        flask.current_app.config['STRIPE_CLIENT_ID']
    )

    if user_info is None:
        return flask.redirect('/')

    stripe_id = user_info['stripe_user_id']

    cur_seller = add_stripe_id(stripe_id)
    flask.session['stripe_id'] = stripe_id

    return flask.redirect('/')

@seller.route('/logout')
def logout():
    flask.session.clear()
    return flask.redirect('/')
