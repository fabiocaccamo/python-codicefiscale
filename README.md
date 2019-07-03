[![Build Status](https://travis-ci.org/fabiocaccamo/python-codicefiscale.svg?branch=master)](https://travis-ci.org/fabiocaccamo/python-codicefiscale)
[![codecov](https://codecov.io/gh/fabiocaccamo/python-codicefiscale/branch/master/graph/badge.svg)](https://codecov.io/gh/fabiocaccamo/python-codicefiscale)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/375ce4fc87dc44e88271f7da9f5f69d1)](https://www.codacy.com/app/fabiocaccamo/python-codicefiscale)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/fabiocaccamo/python-codicefiscale/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/fabiocaccamo/python-codicefiscale/?branch=master)
[![Requirements Status](https://requires.io/github/fabiocaccamo/python-codicefiscale/requirements.svg?branch=master)](https://requires.io/github/fabiocaccamo/python-codicefiscale/requirements/?branch=master)
[![PyPI version](https://badge.fury.io/py/python-codicefiscale.svg)](https://badge.fury.io/py/python-codicefiscale)
[![PyPI downloads](https://img.shields.io/pypi/dm/python-codicefiscale.svg)](https://img.shields.io/pypi/dm/python-codicefiscale.svg)
[![Py versions](https://img.shields.io/pypi/pyversions/python-codicefiscale.svg)](https://img.shields.io/pypi/pyversions/python-codicefiscale.svg)
[![License](https://img.shields.io/pypi/l/python-codicefiscale.svg)](https://img.shields.io/pypi/l/python-codicefiscale.svg)

# python-codicefiscale
python-codicefiscale is a tiny library for encode/decode Italian fiscal code - **codifica/decodifica del Codice Fiscale**.

## Features
- **Transliteration** for name/surname
- **Multiple** birthdate formats (datetime/string) *(you can see all the supported string formats in* `tests/tests.py` *)*
- **Automatic** birthplace city/foreign-country code detection from name
- **Omocodia** support

## Installation
`pip install python-codicefiscale`

## Usage

#### Import
```python
from codicefiscale import codicefiscale
```
#### Encode
```python
codicefiscale.encode(surname='Caccamo', name='Fabio', sex='M', birthdate='03/04/1985', birthplace='Torino')

# 'CCCFBA85D03L219P'
```
#### Decode
```python
codicefiscale.decode('CCCFBA85D03L219P')

# {
#     'code': 'CCCFBA85D03L219P',
#     'sex': 'M',
#     'birthdate': datetime.datetime(1985, 4, 3, 0, 0),
#     'birthplace': {
#         'name': 'TORINO'
#         'province': 'TO',
#         'code': 'L219',
#     },
#     'omocodes': [
#         'CCCFBA85D03L219P',
#         'CCCFBA85D03L21VE',
#         'CCCFBA85D03L2MVP',
#         'CCCFBA85D03LNMVE',
#         'CCCFBA85D0PLNMVA',
#         'CCCFBA85DLPLNMVL',
#         'CCCFBA8RDLPLNMVX',
#         'CCCFBAURDLPLNMVU',
#     ],
#     'raw': {
#         'code': 'CCCFBA85D03L219P',
#         'surname': 'CCC',
#         'name': 'FBA',
#         'birthdate': '85D03',
#         'birthdate_year': '85'
#         'birthdate_month': 'D',
#         'birthdate_day': '03',
#         'birthplace': 'L219',
#         'cin': 'P',
#     },
# }
```

#### Check
```python
codicefiscale.is_valid('CCCFBA85D03L219P')

# True
```
```python
codicefiscale.is_omocode('CCCFBA85D03L219P')

# False
```

### Test

`tox` / `python setup.py test` / `python -m unittest tests.tests`

---

## License
Released under [MIT License](LICENSE).
