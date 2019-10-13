from photo_sell.models.db import db

def init_app(app):
    db.init_app(app)

    # db.drop_all()
    db.create_all()
