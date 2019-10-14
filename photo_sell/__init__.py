from flask import Flask

def create_app(running_tests=False):
    import photo_sell.models
    import photo_sell.routes

    app = Flask(__name__)
    app.app_context().push()
    app.config.from_object('photo_sell.config')
    app.config.from_pyfile('vars.py')

    if running_tests:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        app.config['TESTING'] = True

    models.init_app(app, running_tests)
    routes.init_app(app, running_tests)

    return app
