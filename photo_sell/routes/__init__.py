from photo_sell.routes.home import home
from photo_sell.routes.seller import seller

def init_app(app):
    app.register_blueprint(home)
    app.register_blueprint(seller)
