import utils
from .leonify import getDeviceId, sp_request

def shuffle(string):
    device_id = getDeviceId()

    request = string.split(' ')

    if(len(request) == 1):
        state = 'true'
        type = 'shuffle'
    elif(request[1] == 'off'):
        state = 'false'
        type = 'shuffleoff'

    sp_request('PUT', 'me/player/shuffle', {"device_id" : device_id, "state" : state})
    utils.output('end', 'success', utils.translate(type))