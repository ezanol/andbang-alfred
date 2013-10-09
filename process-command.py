#!/usr/bin/python

import sys
import notification
import settings
import api
import server

user_settings = settings.Settings()

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
    if command == 'ship':
        r = api.method('/tasks/' + params[2] + '/ship', params[1], {}, 'post').json()
        n.notify("Task was shipped", r["title"], r["id"])
    elif command == 'later':
        r = api.method('/tasks/' + params[2] + '/later', params[1], {}, 'post').json()
        n.notify("Task was latered", r["title"], r["id"])
    elif command == 'create':
        r = api.method('/me/tasks', params[1], {'title': params[2]}, 'post').json()
        n.notify("Task was created", r["title"], r["id"])
    elif command == 'activate':
        r = api.method('/tasks/' + params[2] + '/start', params[1], {}, 'post').json()
        n.notify("Task was started", r["title"], r["id"])
    elif command == 'delete':
        r = api.method('/tasks/' + params[2], params[1], {}, 'delete').json()
        n.notify("Task was deleted", r["title"], r["id"])
    else:
        n.notify("No action was specified", "", "")
else:
    n.notify("Number of parameters was incorrect", "", "")