#!/usr/bin/python

import sys
import api
import server
import requests

param_str = sys.argv[1]
params = param_str.split(':')

command = params[0]

if command == 'token':
    if len(params) > 1 and params[1] == 'true':
        server.save_token(True)
    else:
        server.save_token(False)
    sys.exit()

if command == 'teams':
    server.save_teams()
    sys.exit()

if command == 'members':
    server.save_members()
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
        print "Error: no action was specified"

    if r.status_code >= 200 and r.status_code <= 299:
        task = r.json()
        print verb.capitalize() + ' - ' + task['title']
    else:
        error = r.json()
        print "Error: " + error['message']
else:
    print "Error: incorrect arguments"