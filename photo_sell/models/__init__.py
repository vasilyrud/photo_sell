from photo_sell.models.db import db

def init_app(app, running_tests):
    db.init_app(app)

    if running_tests:
        db.drop_all()

    db.create_all()
