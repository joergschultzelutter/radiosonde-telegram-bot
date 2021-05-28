#!/opt/local/bin/python
#
# Telegram Bot "Radiosonde Landing Prediction"
# Uses "radiosonde_modules" from the MPAD project
# (file is 100% identical).
#
# This is mainly a web site scraper which uses predict.habhub.org
# and radiosondy.info as data sources
#
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

import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import ParseMode
from telegram.ext import MessageHandler, Filters
from utility_modules import read_program_config
from radiosonde_modules import get_radiosonde_landing_prediction, get_radiosondy_data
from geopy_modules import get_reverse_geopy_data
import sys
import signal

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(module)s -%(levelname)s- %(message)s"
)
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
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="73 de DF1JSL's/DB4BIN's Telegram radiosonde landing prediction bot",
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Use command <pre>/sonde [radiosonde-id]</pre> for requesting the landing prediction information",
        parse_mode=ParseMode.HTML,
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Source code & further info: https://www.github.com/joergschultzelutter/radiosonde-telegram-bot",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


def sonde(update, context):
    for sonde in context.args:
        sonde = sonde.upper()
        if len(sonde) > 0:
            found_something = False
            # Run the query on habhub.org
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"<i>Querying position data for '{sonde}' on <pre>habhub.org</pre></i>",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
            (
                success,
                lat,
                lon,
                timestamp,
                landing_url,
            ) = get_radiosonde_landing_prediction(
                aprsfi_callsign=sonde, aprsdotfi_api_key=aprsdotfi_api_key
            )
            if success:
                found_something = True
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"<b><u>Habhub information for <i>{sonde}</i></u></b>",
                    parse_mode=ParseMode.HTML,
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"<b>Landing prediction:</b> landing time ={timestamp.strftime('%d-%b-%Y %H:%M:%S')} UTC, latitude = {lat}, longitude={lon} <a href=\"https://maps.google.com/?q={lat},{lon}\">(Google Maps link)</a>",
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
                success, address = get_reverse_geopy_data(latitude=lat, longitude=lon)
                if success and address:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"<b>Address:</b> {address}",
                        parse_mode=ParseMode.HTML,
                    )
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"`<i>Habhub did not provide any data for '{sonde}'`</i>",
                    parse_mode=ParseMode.HTML,
                )
            # Run the query on radiosondy.info
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"<i>Querying position data for '{sonde}' on <pre>radiosondy.info</pre> - this might take a while</i>",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
            success, radiosondy_response_data = get_radiosondy_data(sonde_id=sonde)
            if success:
                found_something = True
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"<b><u>Radiosondy information for '{sonde}'</u></b>",
                    parse_mode=ParseMode.HTML,
                )
                launch_site = radiosondy_response_data["launch_site"]
                if launch_site:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"<b>Launch Site:</b> {launch_site}",
                        parse_mode=ParseMode.HTML,
                    )
                probe_status = radiosondy_response_data["probe_status"]
                if probe_status:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"<b>Probe Status:</b> {probe_status}",
                        parse_mode=ParseMode.HTML,
                    )
                landing_point_latitude = radiosondy_response_data[
                    "landing_point_latitude"
                ]
                landing_point_longitude = radiosondy_response_data[
                    "landing_point_longitude"
                ]
                if landing_point_latitude != 0.0 and landing_point_longitude != 0.0:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f'<b>Landing point:</b> Lat {landing_point_latitude} / Lon {landing_point_longitude} <a href="https://maps.google.com/?q={landing_point_latitude},{landing_point_longitude}">(Google Maps link)</a>',
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
                    success, address = get_reverse_geopy_data(
                        latitude=landing_point_latitude,
                        longitude=landing_point_longitude,
                    )
                    if success and address:
                        context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"<b>Landing point address data:</b> {address}",
                            parse_mode=ParseMode.HTML,
                        )
                else:
                    landing_point = radiosondy_response_data["landing_point"]
                    if landing_point:
                        context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"<b>Landing Point raw coordinates:</b> {landing_point}",
                            parse_mode=ParseMode.HTML,
                        )
                landing_description = radiosondy_response_data["landing_description"]
                if landing_description:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"<b>Landing description:</b> {landing_description}",
                        parse_mode=ParseMode.HTML,
                    )
                latitude = radiosondy_response_data["latitude"]
                longitude = radiosondy_response_data["longitude"]
                if latitude and longitude:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f'<b>Last coordinates on <pre>aprs.fi</pre></b>: Lat {latitude} / Lon {longitude} <a href="https://maps.google.com/?q={latitude},{longitude}">(Google Maps link)</a>',
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
                    success, address = get_reverse_geopy_data(
                        latitude=latitude, longitude=longitude
                    )
                    if success and address:
                        context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"<b><pre>aprs.fi</pre> address data:</b> {address}",
                            parse_mode=ParseMode.HTML,
                        )
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"<i><pre>Radiosondy.info</pre> did not provide any data for '{sonde}'</i>",
                    parse_mode=ParseMode.HTML,
                )
            if not found_something:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Didn't find anything on radiosonde '{sonde}'",
                )


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Unknown command.")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Use command <pre>/sonde [radiosonde-id]</pre> for requesting the landing prediction information",
        parse_mode=ParseMode.HTML,
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Source code & further info: https://www.github.com/joergschultzelutter/radiosonde-telegram-bot",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


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

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    sonde_handler = CommandHandler("sonde", sonde)
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
        logger.info(msg="Have terminated the updater")
