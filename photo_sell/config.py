import os

SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
SECRET_KEY = os.urandom(24)

GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_INFO_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_LOGIN_URL = 'https://oauth2.googleapis.com/tokeninfo'
GOOGLE_DRIVE_THUMBNAIL_URL = 'https://drive.google.com/thumbnail?id='

STRIPE_AUTH_URL = 'https://connect.stripe.com/oauth/authorize'
STRIPE_INFO_URL = 'https://connect.stripe.com/oauth/token'
