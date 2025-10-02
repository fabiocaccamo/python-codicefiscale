[![](https://img.shields.io/pypi/pyversions/python-codicefiscale.svg?logoColor=white&color=blue&logo=python)](https://www.python.org/)
[![](https://img.shields.io/pypi/v/python-codicefiscale.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/python-codicefiscale/)
[![](https://static.pepy.tech/badge/python-codicefiscale/month)](https://pepy.tech/project/python-codicefiscale)
[![](https://img.shields.io/github/stars/fabiocaccamo/python-codicefiscale?logo=github&style=flat)](https://github.com/fabiocaccamo/python-codicefiscale/stargazers)
[![](https://img.shields.io/pypi/l/python-codicefiscale.svg?color=blue&)](https://github.com/fabiocaccamo/python-codicefiscale/blob/main/LICENSE)

[![](https://results.pre-commit.ci/badge/github/fabiocaccamo/python-codicefiscale/main.svg)](https://results.pre-commit.ci/latest/github/fabiocaccamo/python-codicefiscale/main)
[![](https://img.shields.io/github/actions/workflow/status/fabiocaccamo/python-codicefiscale/test-package.yml?branch=main&label=build&logo=github)](https://github.com/fabiocaccamo/python-codicefiscale)
[![](https://img.shields.io/codecov/c/gh/fabiocaccamo/python-codicefiscale?logo=codecov)](https://codecov.io/gh/fabiocaccamo/python-codicefiscale)
[![](https://img.shields.io/codacy/grade/8927f48c9498408f85167da9287edd86?logo=codacy)](https://www.codacy.com/app/fabiocaccamo/python-codicefiscale)
[![](https://img.shields.io/scrutinizer/quality/g/fabiocaccamo/python-codicefiscale?logo=scrutinizer)](https://scrutinizer-ci.com/g/fabiocaccamo/python-codicefiscale/?branch=main)
[![](https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&logoColor=black)](https://github.com/psf/black)
[![](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# python-codicefiscale
python-codicefiscale is a library for encode/decode Italian fiscal code - **codifica/decodifica del Codice Fiscale**.

![Codice Fiscale](https://user-images.githubusercontent.com/1035294/72058207-fa77dd80-32cf-11ea-8995-52324e7d3efe.png)

## Features
- `NEW` **Auto-updated** data (once a week) directly from **ANPR** data-source.
- `NEW` **Command Line Interface** available.
- **Transliteration** for name/surname
- **Multiple** birthdate formats (date/string) *(you can see all the supported string formats [here](https://github.com/fabiocaccamo/python-codicefiscale/blob/main/tests/test_codicefiscale.py#L81-L140))*
- **Automatic** birthplace city/foreign-country code detection from name
- **Omocodia** support

## Installation
`pip install python-codicefiscale`

## Usage

### Python

#### Import
```python
from codicefiscale import codicefiscale
```
#### Encode
```python
codicefiscale.encode(
    lastname="Caccamo",
    firstname="Fabio",
    gender="M",
    birthdate="03/04/1985",
    birthplace="Torino",
)

# "CCCFBA85D03L219P"
```
#### Decode
```python
codicefiscale.decode("CCCFBA85D03L219P")

# {
#     "code": "CCCFBA85D03L219P",
#     "gender": "M",
#     "birthdate": datetime.datetime(1985, 4, 3, 0, 0),
#     "birthplace": {
#         "name": "TORINO"
#         "province": "TO",
#         "code": "L219",
#     },
#     "omocodes": [
#         "CCCFBA85D03L219P",
#         "CCCFBA85D03L21VE",
#         "CCCFBA85D03L2MVP",
#         "CCCFBA85D03LNMVE",
#         "CCCFBA85D0PLNMVA",
#         "CCCFBA85DLPLNMVL",
#         "CCCFBA8RDLPLNMVX",
#         "CCCFBAURDLPLNMVU",
#     ],
#     "raw": {
#         "code": "CCCFBA85D03L219P",
#         "lastname": "CCC",
#         "firstname": "FBA",
#         "birthdate": "85D03",
#         "birthdate_year": "85"
#         "birthdate_month": "D",
#         "birthdate_day": "03",
#         "birthplace": "L219",
#         "cin": "P",
#     },
# }
```

#### Check
```python
codicefiscale.is_valid("CCCFBA85D03L219P")

# True
```
```python
codicefiscale.is_omocode("CCCFBA85D03L219P")

# False
```

### Command Line

> [!CAUTION]
> If sensitive data is written to a log entry it could be exposed to an attacker who gains access to the logs.

This library can be used also as a CLI tool, for more info run:
```bash
python -m codicefiscale --help
```

#### Encode (CLI)
```bash
python -m codicefiscale encode --firstname Fabio --lastname Caccamo --gender M --birthdate 03/04/1985 --birthplace Torino
```

#### Decode (CLI)
```bash
python -m codicefiscale decode CCCFBA85D03L219P
```

## Testing
```bash
# clone repository
git clone https://github.com/fabiocaccamo/python-codicefiscale.git && cd python-codicefiscale

# create virtualenv and activate it
python -m venv venv && . venv/bin/activate

# upgrade pip
python -m pip install --upgrade pip

# install requirements
pip install -r requirements.txt -r requirements-test.txt

# install pre-commit to run formatters and linters
pre-commit install --install-hooks

# run tests using tox
tox

# or run tests using pytest
pytest
```

## License
Released under [MIT License](LICENSE.txt).

---

## Supporting

- :star: Star this project on [GitHub](https://github.com/fabiocaccamo/python-codicefiscale)
- :octocat: Follow me on [GitHub](https://github.com/fabiocaccamo)
- :blue_heart: Follow me on [Bluesky](https://bsky.app/profile/fabiocaccamo.bsky.social)
- :moneybag: Sponsor me on [Github](https://github.com/sponsors/fabiocaccamo)

## See also

- [`python-benedict`](https://github.com/fabiocaccamo/python-benedict) - dict subclass with keylist/keypath support, I/O shortcuts (base64, csv, json, pickle, plist, query-string, toml, xml, yaml) and many utilities. 📘

- [`python-fontbro`](https://github.com/fabiocaccamo/python-fontbro) - friendly font operations. 🧢

- [`python-fsutil`](https://github.com/fabiocaccamo/python-fsutil) - file-system utilities for lazy devs. 🧟‍♂️
