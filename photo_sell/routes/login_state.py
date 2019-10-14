import functools
import flask

def decide_state(**kwargs):
    if 'google_id' in flask.session:
        if 'stripe_id' in flask.session:
            return flask.render_template('index/seller.html', **kwargs)
        return flask.render_template('index/connect.html', **kwargs)
    return flask.render_template('index/home.html', **kwargs)

def check_google_id(f):

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):

        if 'google_id' not in flask.session:
            return flask.redirect(flask.url_for('home.index'))

        return f(*args, **kwargs)

    return decorated_function

def check_stripe_id(f):

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):

        if 'stripe_id' not in flask.session:
            return flask.redirect(flask.url_for('home.index'))

        return f(*args, **kwargs)

    return decorated_function
