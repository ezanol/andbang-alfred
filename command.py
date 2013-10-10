#!/usr/bin/python

import sys
import api
import re
import core
import feedback
import fuzzy
import settings

valid_commands = ['tasks', 'notifications']
user_settings = settings.Settings()
token = user_settings.get('token')
param_str = sys.argv[1]
params = param_str.split(' ')

def icon_path(team):
    return core.storage('team-' + team['name'])

def ac_commands(team_name, is_multi, cmd):
    global valid_commands
    output = []
    if len(cmd) > 0:
        valid_commands = [k for k in valid_commands if cmd in k]
    for cmd in valid_commands:
        ac = ''
        if is_multi == True:
            ac = team_name + ' '
        output.append(feedback.item(title=team_name + ' ' + cmd, autocomplete=ac + '' + cmd, valid=False))

    return output

def ac_teams(user_teams):
    output = []
    for team in user_teams:
        output.append(feedback.item(title="Team: " + team["name"], valid=False, autocomplete=team["name"] + ' ', icon=icon_path(team)))
    feedback.feedback(output)

def feedback_for_team(team, is_multi):
    commands = param_str.replace(team['name'], '').strip().split(' ')
    output = []

    # autocomplete the valid commands
    if valid_commands.count(commands[0]) == 0:
        output = ac_commands(team['name'], is_multi, commands[0])
    # Display tasks
    elif commands[0] == 'tasks':
        tasks = api.cache_method('/me/tasks', team['id'])
        title = ' '.join(commands[1:]).strip()
        if len(commands) > 1 and len(title) > 0:
            output.append(feedback.item(title='Create: ' + title, valid=True, arg='create:' + team['id'] + ':' + title, icon=icon_path(team)))
            tasks = fuzzy.fuzzy_search(title, tasks, lambda x: '%s' % (x['title']))
        for task in tasks:
            output.append(feedback.item(title="Task: " + task['title'], valid=True, arg='ship:' + team['id'] + ':' + task['id'], icon=icon_path(team)))
    elif commands[0] == 'notifications':
        notifications = tasks = api.cache_method('/me/notifications', team['id'])
        for n in notifications:
            output.append(feedback.item(title=n['title'], subtitle=n['body'], valid=False, icon=icon_path(team)))
    feedback.feedback(output)

# Do nothing until there is an access_token
if (token is None or bool(re.search("^[a-z0-9]{128}$", token)) == False) or params[0] == 'token':
    feedback.feedback(feedback.item(title='Get a token', valid=True, arg='token'))
    sys.exit()

# Check that the user has a team
user_teams = user_settings.get('teams', [])
if len(user_teams) == 0 or params[0] == 'teams':
    title = ''
    if len(user_teams) == 0:
        title = 'No'
    else:
        title = 'Update'
    feedback.feedback(feedback.item(title=title + ' teams', autocomplete='teams', subtitle='Use `teams` to update your teams', arg='teams', valid=True))
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
    ac_teams(user_teams)
