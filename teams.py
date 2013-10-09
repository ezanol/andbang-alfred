#!/usr/bin/python

import alp
import requests
import api

n = alp.Notification()
settings = alp.Settings()

def save():
    r = api.method('/me/teams')
    if r.status_code == 200:
        resp = r.json()
        if len(resp) > 0:
            settings.set(teams=resp)
            write_images()
            n.notify("AndBang Workflow Success", "Your teams were saved!", "Teams: " + ', '.join([team["name"] for team in resp]))
        else:
            n.notify("AndBang Workflow Error", "No teams were saved", "Please create one at http://andbang.com")
    else:
        n.notify("AndBang Workflow Error", resp["message"], "Visit http://andbang.com")

def write_images():
    teams = get()
    for team in teams:
        r = requests.get('http:' + team["thumbUrl"], stream=True)
        if r.status_code == 200:
            with open(iconPath(team), 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)

def iconPath(team):
    return alp.storage('team-' + team['name'])

def get():
    return settings.get('teams', [])

def autocomplete():
    output = []
    teams = get()
    for team in teams:
        output.append(alp.Item(title="AndBang Team: " + team["name"], valid=False, autocomplete=team["name"] + ' ', icon=iconPath(team)))
    return alp.feedback(output)