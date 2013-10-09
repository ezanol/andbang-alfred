#!/usr/bin/python

import sys
import alp
import teams
import api
import re

valid_commands = ['tasks', 'notifications']
settings = alp.Settings()
token = settings.get('token')
param_str = sys.argv[1]
params = param_str.split(' ')

def ac_commands(team_name, is_multi):
    output = []
    for cmd in valid_commands:
        ac = ''
        if is_multi == True:
            ac = team_name + ' '
        output.append(alp.Item(title=team_name + ' ' + cmd, autocomplete=ac + '' + cmd, valid=False))
    return output

def feedback_for_team(team, is_multi):
    commands = param_str.replace(team['name'], '').strip().split(' ')
    output = []

    # autocomplete the valid commands
    if valid_commands.count(commands[0]) == 0:
        output = ac_commands(team['name'], is_multi)
    # Display tasks
    elif commands[0] == 'tasks':
        tasks = api.cache_method('/me/tasks', team['id'])
        title = ' '.join(commands[1:]).strip()
        if len(commands) > 1 and len(title) > 0:
            output.append(alp.Item(title='Create: ' + title, valid=True, arg='create:' + team['id'] + ':' + title, icon=teams.iconPath(team)))
            tasks = alp.fuzzy_search(title, tasks, lambda x: '%s' % (x['title']))
        for task in tasks:
            output.append(alp.Item(title="Task: " + task['title'], valid=True, arg='ship:' + team['id'] + ':' + task['id'], icon=teams.iconPath(team)))
    elif commands[0] == 'notifications':
        notifications = tasks = api.cache_method('/me/notifications', team['id'])
        for n in notifications:
            output.append(alp.Item(title=n['title'], subtitle=n['body'], valid=False, icon=teams.iconPath(team)))
    alp.feedback(output)

# Do nothing until there is an access_token
if token is None or bool(re.search("^[a-z0-9]{128}$", token)) == False:
    alp.feedback(alp.Item(title='Get a token', valid=True, arg='token'))
    sys.exit()

# Check that the user has a team
user_teams = teams.get()
if len(user_teams) == 0 or params[0] == 'teams':
    title = ''
    if len(user_teams) == 0:
        title = 'No'
    else:
        title = 'Update'
    alp.feedback(alp.Item(title=title + ' teams', autocomplete='teams', subtitle='Use `teams` to update your teams', arg='teams', valid=True))
    sys.exit()

# There is only one user team so use that
if len(user_teams) == 1:
    team = user_teams[0]
    feedback_for_team(team, False)
    sys.exit()
else:
    # User has multiple teams
    # Check and see if they have specified the name
    for team in user_teams:
        if param_str.find(team['name']) == 0:
            feedback_for_team(team, True)
            sys.exit()

    # Team name was not found in query
    teams.autocomplete()
    sys.exit()
