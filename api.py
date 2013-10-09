import core
import sys
import requests
import json
import glob
import time
import os
import webbrowser
import urllib
import settings

user_settings = settings.Settings()

def method(url, team_id=None, data={}, method='get'):
    api_url = 'https://api.andbang.com:443'
    token = user_settings.get('token', '')
    if team_id != None:
        api_url += '/teams/' + team_id
    api_url += url
    return getattr(requests, method)(api_url, data=json.dumps(data), headers={'Authorization': 'Bearer ' + token})

def save_token():
    import server
    data = {}
    data['client_id'] = 'c85cbe296399c078cbf90eb10ed52a3e0dd8210c'
    data['response_type'] = 'token'
    data['redirect_uri'] = 'http://localhost:3030'
    webbrowser.open('https://accounts.andbang.com/oauth/authorize?' + urllib.urlencode(data))
    server.run(3030)

def cache_method(url, team_id=None):
    api_url = 'https://api.andbang.com:443'
    token = user_settings.get('token')
    if team_id != None:
        api_url += '/teams/' + team_id
    api_url += url

    now = time.time()
    this_cache_name = api_url.split(':443')[1].strip('/').replace('/', '-')
    valid_cache_file = None

    cache_files = glob.glob(core.cache(this_cache_name) + '*')
    for cache_file in cache_files:
        cache_ts = cache_file.replace(core.cache(this_cache_name) + '|', '').split('.')[0]
        time_ago = int(now) - int(cache_ts)
        if time_ago <= 60:
            valid_cache_file = cache_file
            break
    
    resp = None

    if valid_cache_file != None:
        resp = core.jsonLoad(valid_cache_file, [])
        for cache_file in cache_files:
            if cache_file != valid_cache_file:
                os.remove(cache_file)
        return resp
    else:
        r = requests.get(api_url, headers={'Authorization': 'Bearer ' + token})
        if r.status_code == requests.codes.ok:
            resp = r.json()
            core.jsonDump(resp, core.cache(this_cache_name + '|' + str(int(now)) + '.json'))
            return resp
        else:
            resp = r.json()
            core.feedback(core.Item(title="Error: " + resp['message'], arg="token", valid=True))
            sys.exit()

    
