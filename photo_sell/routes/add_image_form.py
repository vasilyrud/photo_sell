import flask

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

class AddImageForm(FlaskForm):
    drive_url = StringField(label='Drive URL', validators=[DataRequired()])

    def validate_drive_url(form, field):
        form._parse_drive_url(field.data)

    def _drive_image_exists(form, drive_id):
        service = build('drive', 'v3', developerKey=flask.current_app.config['GOOGLE_DRIVE_API_KEY'])

        try:
            request = service.files().get_media(fileId=drive_id).execute()
        except HttpError:
            return False

        return True

    def _get_drive_id(form, drive_url, suburl):

        DRIVE_ID_LEN = 28

        find_index = drive_url.find(suburl)

        if find_index == -1:
            return None

        drive_id_start = find_index + len(suburl)
        drive_id_end   = drive_id_start + DRIVE_ID_LEN

        if drive_id_end > len(drive_url):
            return None

        drive_id = drive_url[drive_id_start:drive_id_end]

        if not drive_id.isalnum():
            return None

        return drive_id

    def _parse_drive_url(form, drive_url):
        POSSIBLE_SUBURLS = [
            'drive.google.com/file/d/',
            'drive.google.com/open?id='
        ]

        for possible_suburl in POSSIBLE_SUBURLS:
            drive_id = form._get_drive_id(drive_url, possible_suburl)

            if drive_id is not None:
                break

        if drive_id is None:
            raise ValidationError('Invalid Google Drive URL provided')

        if not form._drive_image_exists(drive_id):
            raise ValidationError('Image does not exist or isn\'t public')

        # TODO: Check if image belongs to user
