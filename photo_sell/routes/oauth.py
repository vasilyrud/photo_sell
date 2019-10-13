import os
import requests
import hashlib

import flask

def _make_redir_uri(service):
    return flask.current_app.config['REDIR_URI_BASE'] + '/' + service + '_auth'

def authorize_url(
    service,
    auth_url,
    scope,
    client_id,
    **kwargs
):

    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    flask.session[service + '_state'] = state

    params = {
        'response_type': 'code',
        'state': state,
        'scope': scope,
        'client_id': client_id,
        'redirect_uri': _make_redir_uri(service),
    }
    params.update(kwargs)

    print('authorize_url params:', params)

    req = requests.Request('GET', 
        auth_url,
        params=params
    ).prepare()

    return req.url

def get_user_info(
    service,
    info_url,
    client_secret,
    client_id,
    **kwargs
):
    state = flask.request.args.get('state')
    print('state:', state)

    if flask.session[service + '_state'] != state:
        print('ERROR: state mismatch')

        # TODO: This redirect will not work
        # TODO: Use `url_for` instead of '/'
        flask.redirect('/')

    code = flask.request.args.get('code')
    print('code:', code)

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_secret': client_secret,
        'client_id': client_id,
        'redirect_uri': _make_redir_uri(service),
    }
    data.update(kwargs)

    resp = requests.post(
        info_url,
        data=data
    )

    resp_data = resp.json()
    print(resp_data)

    if 'error' in resp_data:
        return None

    return resp_data

def authenticate(
    auth_url,
    user_info,
    **kwargs
):
    access_token = user_info['access_token']

    params = {
        'id_token': user_info['id_token'],
    }
    params.update(kwargs)

    validate_id_token = requests.get(
        auth_url,
        params=params
    )

    id_token_data = validate_id_token.json()

    return id_token_data
