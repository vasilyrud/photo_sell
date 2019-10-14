from photo_sell.models.db import db

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String, unique=True, nullable=False)
    stripe_id = db.Column(db.String, unique=True, nullable=True)

    images = db.relationship('Image', backref='seller', lazy=True)

    def __repr__(self):
        return '<Seller: %r>' % self.id

    @classmethod
    def add_google_id(cls, google_id):

        if not db.session.query(db.exists().where(
            cls.google_id == google_id
        )).scalar():
            print('Creating user', google_id)
            db.session.add(cls(google_id=google_id))
            db.session.commit()

        return db.session.query(cls).filter(
            cls.google_id == google_id
        ).first()

    @classmethod
    def add_stripe_id(cls, stripe_id, seller_id):

        cur_seller = db.session.query(cls).filter(
            cls.id == seller_id
        ).first()

        cur_seller.stripe_id = stripe_id
        db.session.commit()

        return cur_seller
