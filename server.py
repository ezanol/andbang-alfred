#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import settings
import urlparse
import webbrowser
import urllib
import api
import requests
import core
import notification as n

run_server = True

#Create custom HTTPRequestHandler class
class HTTPRequestHandler(BaseHTTPRequestHandler):

    #handle GET command
    def do_GET(self):
        global run_server
        parse = urlparse.urlparse(self.path)
        query = urlparse.parse_qs(parse.query)

        self.send_response(200)
        self.send_header('Content-type','text-html')
        self.end_headers()

        message = 'Token was not saved. Please try again.'

        if 'access_token' in query:
            token = query['access_token'][0]
            settings.set(token=token)
            message = 'Token has been saved. You may close this window.'
        
        run_server = False
        refresh_script = "<script>h = window.location.href; !!~h.indexOf('#') ? (window.location.href = h.replace('#', '?')) : document.write('" + message + "');</script>"
        self.wfile.write(refresh_script)
        return

def run(port):
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    while run_server:
        httpd.handle_request()

def save_token():
    data = {}
    data['client_id'] = 'c85cbe296399c078cbf90eb10ed52a3e0dd8210c'
    data['response_type'] = 'token'
    data['redirect_uri'] = 'http://localhost:3030'
    webbrowser.open('https://accounts.andbang.com/oauth/authorize?' + urllib.urlencode(data))
    run(3030)

def save_teams():
    r = api.method('/me/teams')
    if r.status_code == requests.codes.ok:
        teams = r.json()
        if len(teams) > 0:
            settings.set(teams=teams)
            for team in teams:
                save_image('http:' + team["thumbUrl"], 'team-' + team['name'])
            n.notify("AndBang Workflow Success", "Your teams were saved!", "Teams: " + ', '.join([team["name"] for team in teams]))
        else:
            n.notify("AndBang Workflow Error", "No teams were saved", "Please create one at http://andbang.com")
    else:
        n.notify("AndBang Workflow Error", resp["message"], "")

def save_image(path, name):
    r = requests.get(path, stream=True)
    if r.status_code == 200:
        with open(core.storage(name), 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)

def save_members():
    output = []
    teams = settings.get('teams', [])
    for team in teams:
        r = api.method('/members', team['id'])
        if r.status_code == requests.codes.ok:
            members = r.json()
            if len(members) > 0:
                for member in members:
                    print 'save ' + member['username']
                    save_image('http:' + member["smallPicUrl"], 'member-' + member['id'])
                    output.append({your_key: member[your_key] for your_key in ['id', 'username', 'smallPicUrl', 'firstName', 'lastName']})
                settings.set(members=output)
                n.notify("AndBang Workflow Success", "Your teams were saved!", "Teams: " + ', '.join([team["name"] for team in teams]))
            else:
                n.notify("AndBang Workflow Error", "No members were saved", "Have some people join your team!")
        else:
            error = r.json()
            n.notify("AndBang Workflow Error", error["message"], "")
