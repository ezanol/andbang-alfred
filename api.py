import alp
import requests
import json
import glob
import time
import os

settings = alp.Settings()

def method(url, team_id=None, data={}, method="get"):
    api_url = 'https://api.andbang.com:443'
    token = settings.get('token')
    if team_id != None:
        api_url += '/teams/' + team_id
    api_url += url
    return getattr(requests, method)(api_url, data=json.dumps(data), headers={'Authorization': 'Bearer ' + token})

def cache_method(url, team_id=None):
    api_url = 'https://api.andbang.com:443'
    token = settings.get('token')
    if team_id != None:
        api_url += '/teams/' + team_id
    api_url += url

    now = time.time()
    this_cache_name = api_url.split(':443')[1].strip('/').replace('/', '-')
    valid_cache_file = None

    cache_files = glob.glob(alp.cache(this_cache_name) + '*')
    for cache_file in cache_files:
        cache_ts = cache_file.replace(alp.cache(this_cache_name) + '|', '').split('.')[0]
        time_ago = int(now) - int(cache_ts)
        if time_ago <= 60:
            valid_cache_file = cache_file
            break
    
    resp = None

    if valid_cache_file != None:
        resp = alp.jsonLoad(valid_cache_file, [])
        for cache_file in cache_files:
            if cache_file != valid_cache_file:
                os.remove(cache_file)
    else:
        req = requests.get(api_url, headers={'Authorization': 'Bearer ' + token})
        resp = req.json()
        alp.jsonDump(resp, alp.cache(this_cache_name + '|' + str(int(now)) + '.json'))

    return resp
