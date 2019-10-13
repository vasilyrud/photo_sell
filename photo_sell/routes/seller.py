import io
import flask

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

from photo_sell.models.db import db
from photo_sell.models.image import Image
from photo_sell.models.seller import Seller

from photo_sell.routes.oauth import authorize_url, get_user_info, authenticate
from photo_sell.routes.add_image_form import AddImageForm

seller = flask.Blueprint('seller', __name__, template_folder='photo_sell.templates')

def _get_seller(google_id):

    # TODO: move to models

    if not db.session.query(db.exists().where(
        Seller.google_id == google_id
    )).scalar():
        print('Creating user', google_id)
        db.session.add(Seller(google_id=google_id))
        db.session.commit()

    return db.session.query(Seller).filter(
        Seller.google_id == google_id
    ).first()

def _add_stripe_id(stripe_id):

    # TODO: move to models

    cur_seller = db.session.query(Seller).filter(
        Seller.id == flask.session['seller_id']
    ).first()

    cur_seller.stripe_id = stripe_id
    db.session.commit()

    return cur_seller

def _download_image(drive_id):

    service = build('drive', 'v3', developerKey=flask.current_app.config['GOOGLE_DRIVE_API_KEY'])
    request = service.files().get_media(fileId=drive_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

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

    # TODO: Disallow access to this URL

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

    cur_seller = _get_seller(google_id)
    flask.session['seller_id'] = cur_seller.id
    flask.session['google_id'] = google_id

    if cur_seller.stripe_id is not None:
        flask.session['stripe_id'] = cur_seller.stripe_id

    return flask.redirect('/')

@seller.route('/stripe_connect')
def stripe_connect():

    # TODO: Disallow access to this URL

    auth_url = authorize_url(
        'stripe',
        flask.current_app.config['STRIPE_AUTH_URL'],
        'read_write',
        flask.current_app.config['STRIPE_CLIENT_ID']
    )

    return flask.redirect(auth_url)

@seller.route('/stripe_auth')
def stripe_auth():

    # TODO: Disallow access to this URL

    user_info = get_user_info(
        'stripe',
        flask.current_app.config['STRIPE_INFO_URL'],
        flask.current_app.config['STRIPE_CLIENT_SECRET'],
        flask.current_app.config['STRIPE_CLIENT_ID']
    )

    if user_info is None:
        return flask.redirect('/')

    stripe_id = user_info['stripe_user_id']

    cur_seller = _add_stripe_id(stripe_id)
    flask.session['stripe_id'] = stripe_id

    return flask.redirect('/')

@seller.route('/logout')
def logout():

    # TODO: Disallow access to this URL

    flask.session.clear()
    return flask.redirect('/')

@seller.route('/add_image', methods=('GET', 'POST'))
def add_image():

    # TODO: Disallow access to this URL

    form = AddImageForm()

    if form.validate_on_submit():
        print('Form submitted:', form.drive_url.data)
        # _parse_drive_url(form.drive_url.data)
        # return flask.redirect('/')

    return flask.render_template('add.html', form=form)
