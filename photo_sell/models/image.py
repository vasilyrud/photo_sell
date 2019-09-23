from photo_sell.models.common import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.String, unique=True, nullable=False)

    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)

    def __repr__(self):
        return '<Image: %r>' % self.drive_id
