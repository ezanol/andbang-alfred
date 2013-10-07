import alp
import alp.request.requests as requests
import json

settings = alp.Settings()

def method(url, team_id=None, data={}, method="get"):
    api_url = 'https://api.andbang.com:443'
    token = settings.get('token')
    if team_id != None:
        api_url += '/teams/' + team_id
    api_url += url
    return getattr(requests, method)(api_url, data=json.dumps(data), headers={'Authorization': 'Bearer ' + token})
