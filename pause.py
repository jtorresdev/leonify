import utils
from .leonify import getDeviceId, sp_request
    
def pause(request):
    device_id = getDeviceId()
    if device_id:
        sp_request('PUT', 'me/player/pause', {"device_id" : device_id}, {})
        utils.output('end', 'success', utils.translate('pause'))
    else:
        utils.output('end', 'error', utils.translate('spotifynotrunning'))