[![Python Versions](https://img.shields.io/pypi/pyversions/python-codicefiscale.svg?logoColor=white&color=blue&logo=python)](https://www.python.org/)
[![PyPI Version](https://img.shields.io/pypi/v/python-codicefiscale.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/python-codicefiscale/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/python-codicefiscale.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/python-codicefiscale/)
[![Stars](https://img.shields.io/github/stars/fabiocaccamo/python-codicefiscale?logo=github)](https://github.com/fabiocaccamo/python-codicefiscale/)
[![License](https://img.shields.io/pypi/l/python-codicefiscale.svg?color=blue&)](https://github.com/fabiocaccamo/python-codicefiscale/blob/master/LICENSE)

[![Travis Build Status](https://img.shields.io/travis/fabiocaccamo/python-codicefiscale?logo=travis)](https://travis-ci.org/fabiocaccamo/python-codicefiscale)
[![CircleCI Build Status](https://img.shields.io/circleci/build/gh/fabiocaccamo/python-codicefiscale?logo=circleci)](https://circleci.com/gh/fabiocaccamo/python-codicefiscale)
[![Codecov Coverage](https://img.shields.io/codecov/c/gh/fabiocaccamo/python-codicefiscale?logo=codecov)](https://codecov.io/gh/fabiocaccamo/python-codicefiscale)
[![Codacy Code Quality](https://img.shields.io/codacy/grade/375ce4fc87dc44e88271f7da9f5f69d1?logo=codacy)](https://www.codacy.com/app/fabiocaccamo/python-codicefiscale)
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/quality/g/fabiocaccamo/python-codicefiscale?logo=scrutinizer)](https://scrutinizer-ci.com/g/fabiocaccamo/python-codicefiscale/?branch=master)
[![Code Climate Maintainability](https://img.shields.io/codeclimate/maintainability-percentage/fabiocaccamo/python-codicefiscale?logo=code-climate)](https://codeclimate.com/github/fabiocaccamo/python-codicefiscale/)
[![Code Climate Tech Debt](https://img.shields.io/codeclimate/tech-debt/fabiocaccamo/python-codicefiscale?logo=code-climate)](https://codeclimate.com/github/fabiocaccamo/python-codicefiscale/)
[![Requirements Status](https://requires.io/github/fabiocaccamo/python-codicefiscale/requirements.svg?branch=master)](https://requires.io/github/fabiocaccamo/python-codicefiscale/requirements/?branch=master)

# python-codicefiscale
python-codicefiscale is a tiny library for encode/decode Italian fiscal code - **codifica/decodifica del Codice Fiscale**.

![Codice Fiscale](https://user-images.githubusercontent.com/1035294/72058207-fa77dd80-32cf-11ea-8995-52324e7d3efe.png)

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

## Testing
```bash
# create python 3.8 virtual environment
virtualenv testing_codicefiscale -p "python3.8" --no-site-packages

# activate virtualenv
cd testing_codicefiscale && . bin/activate

# clone repo
git clone https://github.com/fabiocaccamo/python-codicefiscale.git src && cd src

# install requirements
pip install --upgrade pip
pip install -r requirements.txt

# run tests using tox
tox

# or run tests using unittest
python -m unittest tests.tests

# or run tests using setuptools
python setup.py test
```

---

## License
Released under [MIT License](LICENSE).
