import utils
import json
from .leonify import getDeviceId, sp_request, getCurrentSong


def play(string):

    request = string.split(' ')

    device_id = getDeviceId()

    if(len(request) == 1):
        sp_request('PUT', 'me/player/play', {'device_id': device_id})
        utils.output('end', 'success', 'Resume')
        exit()
    elif(request[1] == 'album'):
        search_for = ' '.join(request[2:])
        type = 'album,track'
        search_type = 'albums'
    elif(request[1] == 'playlist'):
        search_for = ' '.join(request[2:])
        type = 'playlist,track'
        search_type = 'playlists'
    elif(request[1] == 'artist'):
        search_for = ' '.join(request[2:])
        type = 'artist,track'
        search_type = 'artists'
    else:
        search_for = ' '.join(request[1:])
        type = 'track'
        search_type = 'tracks'

    if device_id:
        if search_for:
            results = sp_request(
                'GET', 'search', {'q': search_for, 'type': type})

            if results[search_type]['total'] > 0 and search_type != 'tracks':
                source = results[search_type]['items'][0]
                by = ''
                type = ''

                data = {}
                data["context_uri"] = source["uri"]

                sp_request('PUT', 'me/player/play',
                           {'device_id': device_id}, json.dumps(data))

                if search_type == 'artists':
                    current_song = getCurrentSong()
                    by = current_song['artists']
                    name = current_song['name']
                else:
                    by_arr = []
                    if 'artists' in source:
                        for artist in source['artists']:
                            by_arr.append(artist['name'])
                    elif 'owner' in source:
                        by_arr.append(source['owner']['display_name'])

                    by = ', '.join(by_arr)
                    name = source['name']
                    type = request[1]

                utils.output('end', 'success', utils.translate('playing', {
                    "name": name,
                    "by": by,
                    "type": type
                }))
            elif results['tracks']['total'] > 0:
                track = results['tracks']['items'][0]
                artists = []
                for artist in track['artists']:
                    artists.append(artist['name'])

                data = {}
                data["uris"] = [track["uri"]]

                sp_request('PUT', 'me/player/play',
                           {'device_id': device_id}, json.dumps(data))

                utils.output('end', 'success', utils.translate('playing', {
                    "name": track['name'],
                    "by":  ', '.join(artists),
                    "type": ""
                }))
            else:
                utils.output('end', 'error', utils.translate('nothingfound'))
    else:
        utils.output('end', 'error', utils.translate('spotifynotrunning'))
