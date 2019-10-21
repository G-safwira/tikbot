#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telegram
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from constants import BOTTOKEN

bot = telegram.Bot(BOTTOKEN)
chats = ['tietokilta','tietokila','tiklors']

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html("hi!"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        event = self.headers.get('X-Discourse-Event')
        data = json.loads(self.rfile.read(int(self.headers.get('content-length'))))
        print(data)
        if event == 'topic_created':
            data = data['topic']
            for c in chats:
            bot.send_message(c, f"""Uusi hakemus!\n{data['title']}""")
        elif event == 'post_created':
            data = data['post']
            for c in chats:
                bot.send_message(c, f"""Uusi viesti ketjuun {data['topic_title']}!\n\nhttps://vaalit.tietokilta.fi/t/{data['topic_slug']}/{data['topic_id']}""")
        self._set_headers()
        self.wfile.write(self._html("POST!"))

if __name__ == "__main__":
    server_address = ("0.0.0.0", 4000)
    httpd = HTTPServer(server_address, S)
    print(f"Starting httpd server on 0.0.0.0:4000")
    httpd.serve_forever()
    print("serv?")

