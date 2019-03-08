import utils 
import webbrowser
from urllib.parse import urlencode

def login(string):
    config = {
        'redirect_uri': utils.config('callback_uri'),
        'response_type': 'code',
        'client_id': utils.config('client_id'),
        'scope': utils.config('scope')
    }

    url = 'https://accounts.spotify.com/authorize?' + urlencode(config)

    webbrowser.open(url)

    utils.output('end', 'success', utils.translate('login'))