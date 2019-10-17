import functools
import flask

def decide_state(*args, **kwargs):
    ''' Decides template to render based on state of the 
    seller, stored in session.

    Only those that are authenticated with Google and have
    authorized us to use their Stripe account are given
    access to a seller's features.

    Args:
        Any arguments are passed on to `render_template`
    '''

    if 'google_id' in flask.session:
        if 'stripe_id' in flask.session:
            return flask.render_template('index/seller.html', *args, **kwargs)
        return flask.render_template('index/connect.html', *args, **kwargs)
    return flask.render_template('index/home.html', *args, **kwargs)

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
