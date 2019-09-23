from photo_sell.models.common import db

def init_app(app):
    db.init_app(app)

    # db.drop_all()
    db.create_all()
