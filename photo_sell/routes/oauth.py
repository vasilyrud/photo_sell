import os
import requests
import hashlib

import flask

class OAuthError(Exception):
   pass

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

    if state is None or state != flask.session[service + '_state']:
        raise OAuthError('State variable mismatch for ' + service + '_state')

    code = flask.request.args.get('code')

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

    if 'error' in resp_data:
        raise OAuthError('Error getting response for ' + service + ' login')

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
