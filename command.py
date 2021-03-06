#!/usr/bin/python

import sys
import api
import re
import core
import feedback
import fuzzy
import settings

valid_commands = ['tasks', 'notifications']
token = settings.get('token', '')
is_first_time = str(token == '').lower()
param_str = sys.argv[1]
params = param_str.split(' ')

def icon_path(team):
    return core.storage('team-' + team['name'])

def icon_path_member(member):
    return core.storage('member-' + member['id'])

def ac_commands(team, is_multi, cmd):
    global valid_commands
    output = []
    if len(cmd) > 0:
        valid_commands = [k for k in valid_commands if cmd in k]
    for cmd in valid_commands:
        ac = ''
        if is_multi == True:
            ac = team['name'] + ' '
        output.append(feedback.item(title=team['name'] + ' ' + cmd, autocomplete=ac + '' + cmd, valid=False, icon=icon_path(team)))

    return output

def ac_teams(user_teams, query=''):
    output = []
    for team in user_teams:
        output.append(feedback.item(title=team["name"], valid=False, autocomplete=team["name"] + ' ', icon=icon_path(team)))
    if query != '':
        output = fuzzy.fuzzy_search(query, output, lambda x: '%s' % (x['content']['title']))
    feedback.feedback(output)

def feedback_for_team(team, is_multi):
    commands = param_str.replace(team['name'], '').replace(team['slug'], '').strip().split(' ')
    output = []

    # autocomplete the valid commands
    if valid_commands.count(commands[0]) == 0:
        output = ac_commands(team, is_multi, commands[0])
    # Display tasks
    elif commands[0] == 'tasks':
        tasks = api.cache_method('/me/tasks', team['id'])
        title = ' '.join(commands[1:]).strip()
        if len(commands) > 1 and len(title) > 0:
            output.append(feedback.item(title='Create: ' + title, valid=True, arg='create:' + team['id'] + ':' + title, icon=icon_path(team)))
            tasks = fuzzy.fuzzy_search(title, tasks, lambda x: '%s' % (x['title']))
        elif len(tasks) == 0:
            output.append(feedback.item(title='You have no tasks', valid=False, icon=icon_path(team)))
        for task in tasks:
            output.append(feedback.item(title="Task: " + task['title'], valid=True, arg='ship:' + team['id'] + ':' + task['id'], icon=icon_path(team)))
    elif commands[0] == 'notifications':
        members = settings.get('members', [])
        notifications = api.cache_method('/me/notifications', team['id'])
        if len(notifications) == 0:
            output.append(feedback.item(title='You have no notifications', valid=False, icon=icon_path(team)))
        for n in notifications:
            m = [member for member in members if member['id'] == n['who']]
            if len(m) >= 1:
                icon = icon_path_member(m[0])
            else:
                icon = icon_path(team)
            output.append(feedback.item(title=n['title'], subtitle=n['body'], valid=False, icon=icon))
    feedback.feedback(output)

# Do nothing until there is an access_token
if (token is None or bool(re.search("^[a-z0-9]{128}$", token)) == False) or params[0] == 'token':
    feedback.feedback(feedback.item(title='Get a token', valid=True, arg='token:' + str(is_first_time)))
    sys.exit()

# Check that the user has a team
user_teams = settings.get('teams', [])
if len(user_teams) == 0 or params[0] == 'teams':
    title = ''
    if len(user_teams) == 0:
        title = 'No'
    else:
        title = 'Update'
    feedback.feedback(feedback.item(title=title + ' teams', autocomplete='teams', subtitle='Use `teams` to update your teams', arg='teams', valid=True))
    sys.exit()

if params[0] == 'members':
    feedback.feedback(feedback.item(title='Update members', autocomplete='members', subtitle='Use `members` to update your team members', arg='members', valid=True))
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
        check_team_name = param_str.lower().strip()
        if check_team_name.find(team['name'].lower()) == 0 or check_team_name.find(team['slug'].lower()) == 0:
            feedback_for_team(team, True)
            sys.exit()

    # Team name was not found in query
    ac_teams(user_teams, check_team_name)
