from photo_sell.routes.home import home
from photo_sell.routes.seller import seller

from photo_sell.routes.cache import cache

def init_app(app, running_tests):
    app.register_blueprint(home)
    app.register_blueprint(seller)

    cache.init_app(app)
