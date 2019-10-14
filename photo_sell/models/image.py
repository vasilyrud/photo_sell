from photo_sell.models.db import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.String, unique=True, nullable=False)

    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)

    def __repr__(self):
        return '<Image: %r>' % self.drive_id

    @classmethod
    def add_drive_image(cls, drive_id, seller_id):

        if not db.session.query(db.exists().where(
            cls.drive_id == drive_id
        )).scalar():
            db.session.add(cls(drive_id=drive_id, seller_id=seller_id))
            db.session.commit()

        return db.session.query(cls).filter(
            cls.drive_id == drive_id
        ).first()
