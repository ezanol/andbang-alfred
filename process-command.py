#!/usr/bin/python

import sys
import notification
import settings
import api
import server
import requests

user_settings = settings.Settings()
n = notification.Notification()

param_str = sys.argv[1]
params = param_str.split(':')

if len(params) < 1:
    sys.exit()

command = params[0]

if command == 'token':
    server.save_token()
    sys.exit()

if command == 'teams':
    server.save_teams()
    sys.exit()

if len(params) == 3:
    verb = ''
    if command == 'ship':
        r = api.method('/tasks/' + params[2] + '/ship', params[1], {}, 'post')
        verb = 'shipped'
    elif command == 'later':
        r = api.method('/tasks/' + params[2] + '/later', params[1], {}, 'post')
        verb = 'latered'
    elif command == 'create':
        r = api.method('/me/tasks', params[1], {'title': params[2]}, 'post')
        verb = 'created'
    elif command == 'activate':
        r = api.method('/tasks/' + params[2] + '/start', params[1], {}, 'post')
        verb = 'activated'
    elif command == 'delete':
        r = api.method('/tasks/' + params[2], params[1], {}, 'delete')
        verb = 'deleted'
    else:
        n.notify("No action was specified", "", "")

    if r.status_code == requests.codes.ok:
        task = r.json()
        n.notify('Task was ' + verb, task['title'], task['id'])
    else:
        error = r.json()
        n.notify('Error with task', error['message'], '')
else:
    n.notify("Number of parameters was incorrect", "", "")