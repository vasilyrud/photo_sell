from photo_sell.models.db import db

class Seller(db.Model):
    ''' Owner of images, who intends to sell them.

    Columns:
        id: Our own ID for the seller.
        google_id: Google's ID for the user.
        stripe_id: Stripe's ID for the user.
        images: Images they are selling.
    '''

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String, unique=True, nullable=False)
    stripe_id = db.Column(db.String, unique=True, nullable=True)

    images = db.relationship('Image', backref='seller', lazy=True)

    def __repr__(self):
        return '<Seller: %r>' % self.id

    @classmethod
    def add_google_id(cls, google_id):
        ''' Return Seller with the given google_id, and
        generate new Seller, if none exists yet.
        '''

        if not db.session.query(db.exists().where(
            cls.google_id == google_id
        )).scalar():
            db.session.add(cls(google_id=google_id))
            db.session.commit()

        return db.session.query(cls).filter(
            cls.google_id == google_id
        ).first()

    @classmethod
    def add_stripe_id(cls, stripe_id, seller_id):
        ''' Return seller with the given ID, and
        link the Stripe ID to them in the database.
        '''

        cur_seller = db.session.query(cls).filter(
            cls.id == seller_id
        ).first()

        cur_seller.stripe_id = stripe_id
        db.session.commit()

        return cur_seller
