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
    ''' Returns a URL that can be used to initiate authorization
    with `service`.

    Args:
        service: Name of service (used to correlate `state` 
            in the cookie with server's own state). Should be
            same when calling `authorize_url` and `get_user_info`.
        auth_url: The OAuth v2 authorize URL of the service.
        scope: Scope specific to the authorization request.
        client_id: Our client ID registered with the service.
    '''

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
    ''' Get token from service after receiving authorization.

    Args:
        service: Must be same as in the `authorize_url` call.
        info_url: a.k.a. the "token" URL.
        client_secret: Our secret, registered with the service.
        client_id: Our client ID registered with the service.
    
    Returns:
        Parsed json data from the info_url.
    '''

    state = flask.request.args.get('state')
    if state is None or state != flask.session[service + '_state']:
        raise OAuthError('State variable mismatch for ' + service + '_state')

    code = flask.request.args.get('code')
    if code is None:
        raise OAuthError('"code" not present in request')

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
    ''' Perform verification of token for the purpose
    of authenticating the user.

    Args:
        auth_url: URL that can perform authentication.
        user_info: Information returned by `get_user_info`.

    Returns:
        Parsed json data from authentication server,
        including the ID of the Google user.
    '''

    access_token = user_info['access_token']

    params = {
        'id_token': user_info['id_token'],
    }
    params.update(kwargs)

    validate_id_token = requests.get(
        auth_url,
        params=params
    )

    return validate_id_token.json()
