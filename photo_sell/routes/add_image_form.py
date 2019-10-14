import flask

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

class AddImageForm(FlaskForm):

    drive_url = StringField(label='Drive URL', validators=[DataRequired()])

    @property
    def drive_id(self):
        return self._parse_drive_url(self.drive_url.data)

    def _get_drive_id(self, raw_drive_url, suburl):

        DRIVE_ID_LEN = 28

        find_index = raw_drive_url.find(suburl)

        if find_index == -1:
            return None

        drive_id_start = find_index + len(suburl)
        drive_id_end   = drive_id_start + DRIVE_ID_LEN

        if drive_id_end > len(raw_drive_url):
            return None

        drive_id = raw_drive_url[drive_id_start:drive_id_end]

        if not drive_id.isalnum():
            return None

        return drive_id

    def _parse_drive_url(self, raw_drive_url):

        POSSIBLE_SUBURLS = [
            'drive.google.com/file/d/',
            'drive.google.com/open?id='
        ]

        for possible_suburl in POSSIBLE_SUBURLS:
            drive_id = self._get_drive_id(raw_drive_url, possible_suburl)

            if drive_id is not None:
                return drive_id

        return None

    def _drive_image_exists(self, drive_id):
        service = build('drive', 'v3', developerKey=flask.current_app.config['GOOGLE_DRIVE_API_KEY'])

        try:
            request = service.files().get_media(fileId=drive_id).execute()
        except HttpError:
            return False

        return True

    def validate_drive_url(self, field):

        drive_id = self._parse_drive_url(field.data)

        if drive_id is None:
            raise ValidationError('Invalid Google Drive URL provided')

        if not self._drive_image_exists(drive_id):
            raise ValidationError('Image does not exist or isn\'t public')

        # TODO: Check if image belongs to current Google user
