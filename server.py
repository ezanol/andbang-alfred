#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import settings
import teams
import urlparse
import webbrowser
import urllib

user_settings = settings.Settings()
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
            user_settings.set(token=token)
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
