import utils
from tinydb import TinyDB, Query
import base64
import requests
import json
import time
import six

def authorize(url):
    db = utils.db()['db']

    code = url.split("?code=")[1].split("&")[0]
    payload = {'redirect_uri': utils.config('callback_uri'),
                   'code': code,
                   'grant_type': 'authorization_code',
                   'scope': utils.config('scope')}
    
    auth_header = base64.b64encode(six.text_type(utils.config('client_id') + ':' + utils.config('client_secret')).encode('ascii'))
    headers = {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

    results = requests.post('https://accounts.spotify.com/api/token', data=payload, headers=headers)

    token_info = results.json()

    token_info['expires_at'] = int(time.time()) + token_info['expires_in']

    token_info['client_id'] = utils.config('client_id')

    token_info['client_secret'] = utils.config('client_secret')

    token_info['prefix'] = utils.config('prefix')

    token_info['scope'] = utils.config('scope')

    db.insert(token_info)

    utils.output('end', 'success', utils.translate('logged'))