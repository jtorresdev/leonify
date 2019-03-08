import utils
from .leonify import getDeviceId, sp_request, getCurrentSong

def next(request):
    device_id = getDeviceId()
    if device_id:
        sp_request('POST', 'me/player/next', {"device_id": device_id})
        current_song = getCurrentSong()
        utils.output('end', 'success', utils.translate('next', {
            "name": current_song['name'],
            "by":  current_song['artists']
        }))
