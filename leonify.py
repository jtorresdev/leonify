import utils
import time
from tinydb import TinyDB, Query
import requests
import json
import base64
import socket
from urllib.parse import urlencode
import webbrowser
import six

db = utils.db()['db']
data = db.all()[0]

access_token = data['access_token']
expires_at = data['expires_at']
refresh_token = data['refresh_token']
client_id = data['client_id']
client_secret = data['client_secret']
prefix = data['prefix']


def getAccessToken():
    global access_token

    now = int(time.time())

    if expires_at - now < 60:
        access_token = refreshAccessToken(refresh_token, db)

    return access_token


def refreshAccessToken(refresh_token, db):
    payload = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}

    auth_header = base64.b64encode(six.text_type(
        client_id + ':' + client_secret).encode('ascii'))

    headers = {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

    response = requests.post(
        'https://accounts.spotify.com/api/token', data=payload, headers=headers)

    token_info = response.json()
    db.update({"access_token": token_info['access_token']})
    return token_info['access_token']


def sp_request(method, endpoint, query_params, body_params={}):
    access_token = getAccessToken()
    url = prefix + endpoint + '?' + urlencode(query_params)
    r = requests.request(method=method, url=url, headers={'Authorization': 'Bearer {0}'.format(
        access_token), 'Content-Type': 'application/json'}, data=body_params)

    if r.text and len(r.text) > 0 and r.text != 'null':
        results = r.json()
        return results
    else:
        return None


def getDeviceId():
    access_token = getAccessToken()
    url = prefix + 'me/player/devices'
    devices = requests.get(
        url=url, headers={'Authorization': 'Bearer {0}'.format(access_token)}).json()
    current_device_name = socket.gethostname()
    device_id = False
    for device in devices['devices']:
        if (device['name'] == current_device_name):
            device_id = device['id']
    return device_id

def getCurrentSong():
    data = {}
    currently_playing = sp_request('GET', 'me/player/currently-playing', {})['item']

    data['name'] = currently_playing['name']

    artists = []

    for artist in currently_playing['artists']:
        artists.append(artist['name'])

    data['artists'] = ', '.join(artists)

    return data