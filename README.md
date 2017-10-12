[![Build Status](https://travis-ci.org/fabiocaccamo/python-codicefiscale.svg?branch=master)](https://travis-ci.org/fabiocaccamo/python-codicefiscale)
[![codecov](https://codecov.io/gh/fabiocaccamo/python-codicefiscale/branch/master/graph/badge.svg)](https://codecov.io/gh/fabiocaccamo/python-codicefiscale)
[![Code Health](https://landscape.io/github/fabiocaccamo/python-codicefiscale/master/landscape.svg?style=flat)](https://landscape.io/github/fabiocaccamo/python-codicefiscale/master)
[![PyPI version](https://badge.fury.io/py/python-codicefiscale.svg)](https://badge.fury.io/py/python-codicefiscale)
[![Py versions](https://img.shields.io/pypi/pyversions/python-codicefiscale.svg)](https://img.shields.io/pypi/pyversions/python-codicefiscale.svg)
[![License](https://img.shields.io/pypi/l/python-codicefiscale.svg)](https://img.shields.io/pypi/l/python-codicefiscale.svg)

# python-codicefiscale
python-codicefiscale is a tiny library for encode/decode Italian fiscal code - **codifica/decodifica del Codice Fiscale**.

## Features
- **Transliteration** for name/surname
- **Multiple** birthdate formats (datetime/string) *(you can see all the supported string formats in* `tests/tests.py` *)*
- **Automatic** birthplace city/country code detection
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
#     'birthdate': datetime(1985, 4, 3), 
#     'birthplace': {
#         'province': 'TO', 
#         'code': 'L219', 
#         'name': 'TORINO', 
#     }, 
#     'cin': 'P',
# }
```

#### Check
```python
codicefiscale.is_valid('CCCFBA85D03L219P')

# True
```

#### Test

`tox` / `python setup.py test` / `python -m unittest tests.tests` 

---

## License
Released under [MIT License](LICENSE).
