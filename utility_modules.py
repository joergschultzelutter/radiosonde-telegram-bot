# Various utility routines
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

import configparser
import os.path
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(module)s -%(levelname)s- %(message)s"
)
logger = logging.getLogger(__name__)


def check_if_file_exists(file_name: str):
    """
    Simple wrapper for whether a file exists or not

    Parameters
    ==========
    file_name: 'str'
        file whose presence we want to check

    Returns
    =======
    _: 'bool'
        True if file exists
    """

    return os.path.isfile(file_name)


def read_program_config(config_file_name: str = "radiosonde.cfg"):
    """
    Read the configuration file and extract the parameter values

    Parameters
    ==========
    config_file_name: 'str'
        file whose presence we want to check

    Returns
    =======
    success: 'bool'
        True if all file exists and there was no issue with extracting
        the values from the config file
    aprsdotfi_cfg_key: 'str'
        aprs.fi API key
    telegram_token: 'str'
        Telegram Bot token
    """

    config = configparser.ConfigParser()
    success = False
    aprsdotfi_cfg_key = telegram_token = None
    if check_if_file_exists(config_file_name):
        try:
            config.read(config_file_name)
            aprsdotfi_cfg_key = config.get("radiosonde_config", "aprsdotfi_api_key")
            telegram_token = config.get(
                "radiosonde_config", "telegram_token"
            )
            success = True
        except:
            success = False
    return (
        success,
        aprsdotfi_cfg_key,
        telegram_token,
    )

if __name__ == "__main__":
    logger.info(read_program_config())