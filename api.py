import core
import sys
import requests
import json
import glob
import time
import os
import settings
import re
import feedback

def method(url, team_id=None, data={}, method='get'):
    token = settings.get('token', '')
    api_url = get_api_url(url, team_id)
    if method != 'get':
        if api_url.find('/tasks') > -1:
            # remove me-tasks caches
            if api_url.find('/me/') == -1:
                cache_url = api_url.split('/tasks/')[0] + '/me/tasks'
            else:
                cache_url = api_url
            remove_cache_files(get_cache_files(get_cache_name(cache_url)))
    return getattr(requests, method)(api_url, data=json.dumps(data), headers={'Authorization': 'Bearer ' + token})

def get_api_url(url, team_id=None):
    api_url = 'https://api.andbang.com:443'
    if team_id != None:
        api_url += '/teams/' + team_id
    api_url += url
    return api_url

def get_cache_name(url):
    return url.split(':443')[1].strip('/').replace('/', '-')

def get_cache_files(name):
    return glob.glob(core.cache(name) + '*')

def cache_method(url, team_id=None):
    now = time.time()
    this_cache_name = get_cache_name(get_api_url(url, team_id))
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
        r = method(url, team_id)
        resp = r.json()
        if r.status_code == 200:
            remove_cache_files(cache_files)
            core.jsonDump(resp, core.cache(this_cache_name + '|' + str(int(now)) + '.json'))
            return resp
        elif r.status_code == 400 and resp['message'] == 'This access token has expired.':
            feedback.feedback(feedback.item(title='You need to refresh your token', subtitle="Select to refresh your token", valid=True, arg='token:false'))
            sys.exit()
        elif r.status_code == 404 and resp['message'] == 'Um, so we need a valid id to lookup access tokens':
            feedback.feedback(feedback.item(title='You need an access token', subtitle="Select to retrieve a token", valid=True, arg='token:true'))
            sys.exit()
        else:
            feedback.feedback(feedback.item(title='There was a problem with the API', subtitle=resp['message'], valid=False))
            sys.exit()

def remove_cache_files(cache_files, valid=None):
    for cache_file in cache_files:
        if cache_file != valid:
            os.remove(cache_file)