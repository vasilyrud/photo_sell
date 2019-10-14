import functools
import flask

def decide_state():
    if 'google_id' in flask.session:
        if 'stripe_id' in flask.session:
            return flask.render_template('index/seller.html')
        return flask.render_template('index/connect.html')
    return flask.render_template('index/home.html')

def check_google_id(f):

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):

        if 'google_id' not in flask.session:
            return flask.redirect('/')

        return f(*args, **kwargs)

    return decorated_function

def check_stripe_id(f):

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):

        if 'stripe_id' not in flask.session:
            return flask.redirect('/')

        return f(*args, **kwargs)

    return decorated_function
