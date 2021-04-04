#
# Author: Joerg Schultze-Lutter, 2020
#
# Purpose: uses Geopy /Nominatim in order to translate lat/lon to
# to address data
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

from geopy.geocoders import Nominatim
import logging
import requests

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(module)s -%(levelname)s- %(message)s"
)
logger = logging.getLogger(__name__)


def get_reverse_geopy_data(
    latitude: float,
    longitude: float,
    language: str = "en",
):
    """
    Get human-readable address data for a lat/lon combination
    ==========
    latitude: 'float'
        Latitude
    longitude: 'float'
        Longitude
    language: 'str'
        iso3166-2 language code

    Returns
    =======
    success: 'bool'
        True if query was successful
    address: 'str'
        full-blown address information from OSM
    """

    address = None

    #
    # Default user agent for accessing aprs.fi, openstreetmap et al
    default_user_agent = f"radiosonde-telegram-bot (+https://github.com/joergschultzelutter/radiosonde-telegram-bot/)"

    # Geopy Nominatim user agent
    geolocator = Nominatim(user_agent=default_user_agent)

    success = True
    try:
        # Lookup with zoom level 18 (building)
        location = geolocator.reverse(
            query=f"{latitude} {longitude}",
            language=language,
            zoom=18,
            addressdetails=True,
            exactly_one=True,
        )
    except:
        location = None
        success = False
    if location:
        address = location.address

    return success, address

if __name__ == "__main__":
    logger.info(get_reverse_geopy_data(latitude=37.7790262, longitude=-122.4199061))
