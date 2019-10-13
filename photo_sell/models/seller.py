from photo_sell.models.db import db

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String, unique=True, nullable=False)
    stripe_id = db.Column(db.String, unique=True, nullable=True)

    images = db.relationship('Image', backref='seller', lazy=True)

    def __repr__(self):
        return '<Seller: %r>' % self.id
