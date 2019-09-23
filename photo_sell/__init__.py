from flask import Flask

def create_app():
    import photo_sell.models
    import photo_sell.routes

    app = Flask(__name__)
    app.app_context().push()
    app.config.from_object('photo_sell.config')
    app.config.from_pyfile('vars.py')

    models.init_app(app)
    routes.init_app(app)

    return app
