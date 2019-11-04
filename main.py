#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telegram
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
from telegram.ext import Updater, CommandHandler

from constants import BOTTOKEN
from messages import NEWCOMMENT, NEWTHREAD
bot = telegram.Bot(BOTTOKEN)

def load_chats():
    with open('channels.json', 'r') as fp:
        return json.load(fp)

def save_channels(chats):
    with open('channels.json', 'w') as fp:
        chats = list(set(chats))
        json.dump(chats, fp)

def start(update, context):
    """Send a message when the command /start is issued."""
    chats = load_chats()
    chats.append( str( update.message.chat_id ) )
    save_channels(chats)
    update.message.reply_text('Chat registered!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def tg_bot():
    print("starting bot")
    """Start the bot."""
    updater = Updater(BOTTOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # Start the Bot
    updater.start_polling()
    updater.idle()

def http_api():
    server_address = ("0.0.0.0", 4000)
    httpd = HTTPServer(server_address, S)
    print(f"Starting httpd server on 0.0.0.0:4000")
    httpd.serve_forever()

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
        chats = load_chats()

        save = False
        # Doesn't do anything with posted data
        event = self.headers.get('X-Discourse-Event')
        data = json.loads(self.rfile.read(int(self.headers.get('content-length'))))
        print(data)
        nchats = []
        if event == 'topic_created':
            data = data['topic']
            if data['title'] != "Aion hakea virkaan":
                for c in chats:
                    try:
                        bot.send_message(c, NEWTHREAD.format(data['title']), parse_mode="Markdown" )
                        nchats.append(c)
                    except:
                        save = True
        elif event == 'post_created':
            data = data['post']
            if data['topic_title'] != "Aion hakea virkaan":
                for c in chats:
                    try:
                        bot.send_message(c, NEWCOMMENT.format(data['topic_title'], data['topic_slug'], data['topic_id']), parse_mode="Markdown")
                        nchats.append(c)
                    except:
                        save = True
                chats = nchats
        if save:
            save_channels(chats)
        self._set_headers()
        self.wfile.write(self._html("POST!"))

if __name__ == "__main__":
    x = threading.Thread(target=http_api)
    x.start()
    tg_bot()

