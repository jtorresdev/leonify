import utils
from .leonify import getDeviceId, sp_request, getCurrentSong

def previous(request):
    device_id = getDeviceId()
    if device_id:
        sp_request('POST', 'me/player/previous', {"device_id": device_id})
        current_song = getCurrentSong()
        utils.output('end', 'success', utils.translate('previous', {
            "name": current_song['name'],
            "by":  current_song['artists']
        }))
