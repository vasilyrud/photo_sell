import io
import flask

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

from photo_sell.models.db import db
from photo_sell.models.image import Image
from photo_sell.models.seller import Seller

from photo_sell.routes.oauth import authorize_url, get_user_info, authenticate, OAuthError
from photo_sell.routes.add_image_form import AddImageForm
from photo_sell.routes.login_state import check_google_id, check_stripe_id, decide_state

seller = flask.Blueprint('seller', __name__, template_folder='photo_sell.templates')

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

    try:
        user_info = get_user_info(
            'google',
            flask.current_app.config['GOOGLE_INFO_URL'],
            flask.current_app.config['GOOGLE_CLIENT_SECRET'],
            flask.current_app.config['GOOGLE_CLIENT_ID']
        )
    except OAuthError:
        return flask.redirect(flask.url_for('home.index'))

    id_token_data = authenticate(
        flask.current_app.config['GOOGLE_LOGIN_URL'],
        user_info
    )

    google_id = id_token_data['sub']

    cur_seller = Seller.add_google_id(google_id)
    flask.session['seller_id'] = cur_seller.id
    flask.session['google_id'] = google_id

    if cur_seller.stripe_id is not None:
        flask.session['stripe_id'] = cur_seller.stripe_id

    return flask.redirect(flask.url_for('home.index'))

@seller.route('/stripe_connect')
@check_google_id
def stripe_connect():

    auth_url = authorize_url(
        'stripe',
        flask.current_app.config['STRIPE_AUTH_URL'],
        'read_write',
        flask.current_app.config['STRIPE_CLIENT_ID']
    )

    return flask.redirect(auth_url)

@seller.route('/stripe_auth')
@check_google_id
def stripe_auth():

    try:
        user_info = get_user_info(
            'stripe',
            flask.current_app.config['STRIPE_INFO_URL'],
            flask.current_app.config['STRIPE_CLIENT_SECRET'],
            flask.current_app.config['STRIPE_CLIENT_ID']
        )
    except OAuthError:
        return flask.redirect(flask.url_for('home.index'))

    stripe_id = user_info['stripe_user_id']

    cur_seller = Seller.add_stripe_id(stripe_id, flask.session['seller_id'])
    flask.session['stripe_id'] = stripe_id

    return flask.redirect(flask.url_for('home.index'))

@seller.route('/logout')
@check_google_id
def logout():

    flask.session.clear()
    return flask.redirect(flask.url_for('home.index'))

@seller.route('/add_image', methods=('GET', 'POST'))
@check_stripe_id
def add_image():

    form = AddImageForm()

    if form.validate_on_submit():
        print('Form submitted:', form.drive_url.data)

        cur_image = Image.add_drive_image(form.drive_id, flask.session['seller_id'])

        return flask.redirect(flask.url_for('home.index'))

    return flask.render_template('add.html', form=form)
