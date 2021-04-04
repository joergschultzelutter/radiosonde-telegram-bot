# Telegram Bot zum Testen der Radiosonde Landing Prediction für DB4BIN
# (jede Menge recycelter Code aus MPAD)
# "radiosonde_modules" ist dabei 1:1 austauschbar
# 
# Ziel: besseres Testen für Ingo :-)
# Author: Joerg Schultze-Lutter, 2020
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import requests
import json
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from utility_modules import read_program_config
from radiosonde_modules import get_radiosonde_landing_prediction
from geopy_modules import get_reverse_geopy_data
import sys
import signal

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(module)s -%(levelname)s- %(message)s")
logger = logging.getLogger(__name__)

def signal_term_handler(signal_number, frame):
    """
    Signal handler for SIGTERM signals. Ensures that the program
    gets terminated in a safe way, thus allowing all databases etc
    to be written to disc.

    Parameters
    ==========
    signal_number:
        The signal number
    frame:
        Signal frame

    Returns
    =======
    """

    logger.info(msg="Received SIGTERM; forcing clean program exit")
    sys.exit(0)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ich bin ein Testbot für DB4BIN")

def sonde(update, context):
    for sonde in context.args:
        sonde = sonde.upper()
        if len(sonde) > 0:
            success, lat, lon, timestamp = get_radiosonde_landing_prediction(aprsfi_callsign=sonde,aprsdotfi_api_key=aprsdotfi_api_key)
            if success:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Landevorhersage: Latitude = {lat}, Longitude={lon}, Landezeit ={timestamp.strftime('%d-%b-%Y %H:%M:%S')} UTC")
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"https://maps.google.com/?q={lat},{lon}")
                success, address = get_reverse_geopy_data(latitude=lat,longitude=lon,language="de")
                if success:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=address)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Nuschel nicht so. Ich verstehe Dich nicht")

if __name__ == "__main__":
    success, aprsdotfi_api_key, telegram_token = read_program_config()
    if not success:
        logger.info("Cannot read config file")
        exit(0)

    # Register the SIGTERM handler; this will allow a safe shutdown of the program
    logger.info(msg="Registering SIGTERM handler for safe shutdown...")
    signal.signal(signal.SIGTERM, signal_term_handler)

    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    sonde_handler = CommandHandler('sonde', sonde)
    dispatcher.add_handler(sonde_handler)

    # must be last handler prior to polling start
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    try:
        updater.start_polling()
    except (KeyboardInterrupt, SystemExit):
        logger.info(
            msg="KeyboardInterrupt or SystemExit in progress; shutting down ..."
        )
        updater.stop()