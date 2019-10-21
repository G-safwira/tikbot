#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
from telegram.ext import Updater

from constants import BOTTOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update):
    logger.warning('Update "%s" caused error "%s"', bot, update.error)

def main():
    updater = Updater(BOTTOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # log all errors
    dp.add_error_handler(error)

    updater.start_webhook(listen='0.0.0.0', port=4000)
    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    #init users
    main()
