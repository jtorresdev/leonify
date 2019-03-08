import utils
from .leonify import getDeviceId, sp_request

def repeat(string):
    device_id = getDeviceId()

    request = string.split(' ')

    if device_id:
        if(len(request) == 1):
            state = 'track'
            type = 'repeat'
        elif(request[1] == 'off'):
            state = 'off'
            type = 'repeatoff'

        sp_request('PUT', 'me/player/repeat', {"device_id" : device_id, "state" : state})
        utils.output('end', 'success', utils.translate(type))