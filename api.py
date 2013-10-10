import core
import sys
import requests
import json
import glob
import time
import os
import settings
import re

def method(url, team_id=None, data={}, method='get'):
    api_url = 'https://api.andbang.com:443'
    token = settings.get('token', '')
    if team_id != None:
        api_url += '/teams/' + team_id
    api_url += url
    if method != 'get':
        if api_url.find('/tasks') > -1:
            # remove me-tasks caches
            cache_url = api_url.split('/tasks/')[0] + '/me/tasks'
            remove_cache_files(get_cache_files(get_cache_name(cache_url)))
    return getattr(requests, method)(api_url, data=json.dumps(data), headers={'Authorization': 'Bearer ' + token})

def get_cache_name(url):
    return url.split(':443')[1].strip('/').replace('/', '-')

def get_cache_files(name):
    return glob.glob(core.cache(name) + '*')

def cache_method(url, team_id=None):
    api_url = 'https://api.andbang.com:443'
    token = settings.get('token')
    if team_id != None:
        api_url += '/teams/' + team_id
    api_url += url

    now = time.time()
    this_cache_name = get_cache_name(api_url)
    valid_cache_file = None

    cache_files = get_cache_files(this_cache_name)
    for cache_file in cache_files:
        cache_ts = cache_file.replace(core.cache(this_cache_name) + '|', '').split('.')[0]
        time_ago = int(now) - int(cache_ts)
        if time_ago <= 60:
            valid_cache_file = cache_file
            break
    
    resp = None

    if valid_cache_file != None:
        resp = core.jsonLoad(valid_cache_file, [])
        remove_cache_files(cache_files, valid_cache_file)
        return resp
    else:
        r = requests.get(api_url, headers={'Authorization': 'Bearer ' + token})
        if r.status_code == requests.codes.ok:
            resp = r.json()
            remove_cache_files(cache_files)
            core.jsonDump(resp, core.cache(this_cache_name + '|' + str(int(now)) + '.json'))
            return resp
        else:
            resp = r.json()
            core.feedback(core.Item(title="Error: " + resp['message'], arg="token", valid=True))
            sys.exit()

def remove_cache_files(cache_files, valid=None):
    for cache_file in cache_files:
        if cache_file != valid:
            os.remove(cache_file)