# radiosonde-telegram-bot
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![CodeQL](https://github.com/joergschultzelutter/radiosonde-telegram-bot/actions/workflows/codeql.yml/badge.svg)](https://github.com/joergschultzelutter/radiosonde-telegram-bot/actions/workflows/codeql.yml)

Radiosonde landing prediction Telegram bot


## Usage
Use the command ```/sonde [radiosonde]``` for running your prediction on a specific radiosonde. The bot will use the given radiosonde ID and run queries on the following web sites:

- predict.habhub.org
- radiosondy.info

Each site gets queried individually.

## Dependencies

### Python packages

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [activesoup](https://github.com/jelford/activesoup) required: version 0.3.0 or greater
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
- [geopy](https://github.com/geopy/geopy)
- [requests](https://github.com/psf/requests)
- [xmltodict](https://github.com/martinblech/xmltodict)

### Web sites

- predict.habhub.org
- radiosondy.info
- aprs.fi

### API access keys

- aprs.fi API access key
- your own telegram API access key

(both need to be stored in the ```radiosonde.cfg``` file)
