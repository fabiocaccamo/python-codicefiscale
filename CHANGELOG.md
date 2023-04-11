# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.0](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.8.0) - 2023-04-09
-   Manage correctly deleted countries. #36
-   Replace `flake8` with `Ruff`.
-   Switch from `setup.cfg` to `pyproject.toml`.
-   Improve code quality.
-   Bump requirements.

## [0.7.1](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.7.1) - 2023-03-30
-   Fix encoding/decoding error when year of birth (excluding century) < 10 (eg. 2004). #79
-   Improve error message for invalid birthplace codes.
-   Refactor tests and move each issue test to its own test case.
-   Update pre-commit hooks. (#80)

## [0.7.0](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.7.0) - 2023-03-27
-   Add command line usage support. #14 (#78)
-   Rename arguments and output variable names: `name` -> `firstname` and `surname` -> `lastname`.

## [0.6.1](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.6.1) - 2023-01-12
-   Add `setup.cfg` (`setuptools` declarative syntax) generated using `setuptools-py2cfg`.
-   Add `pyupgrade` to `pre-commit` config.
-   Remove `tests/` from dist.
-   Updated `countries.json` and `municipalities.json` data.
-   Improve update script error messages and fix formatting error.
-   Bump requirements.

## [0.6.0](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.6.0) - 2022-12-09
-   Add `Python 3.11` support.
-   Add `pre-commit`.
-   Add `pypy` to CI.
-   Drop `Python < 3.8` support.
-   Updated `countries.json` and/or `municipalities.json` data.
-   Replace `str.format` with `f-strings`.
-   Remove encoding pragma.
-   Decrease dependence on `CODICEFISCALE_RE` regex by naming subpatterns.
-   Fix decoding code with invalid birthplace code. #27
-   Fix date of birth not honored when encoding and decoding (deleted municipalities only). #37 (#40)
-   Bump requirements and GitHub actions versions.

## [0.5.0](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.5.0) - 2022-09-22
-   Add municipality validity date support. Fix #12 and #23 by [danisana](https://github.com/danisana) in #24.
-   Replace `str.format` with `f-strings`.
-   Update `countries.json` and `municipalities.json` data.
-   Update and pin requirements.

## [0.4.0](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.4.0) - 2022-02-18
-   Dropped python 2.7 and python 3.5 support.
-   Pinned requirements versions.
-   Moved data to external json files and removed data python module.
-   Updated `countries.json` and `municipalities.json` data.

## [0.3.9](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.3.9) - 2022-01-28
-   Fixed municipality overwritten by old municipality *(deleted)* with the same code. #16

## [0.3.8](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.3.8) - 2022-01-10
-   Fixed number of omocodes. #13
-   Formatted code with **Black**.
-   Updated strings formatting.
-   Added `python 3.9` and `python 3.10` official support.
-   Added `requirements.txt` and `requirements-test.txt`.
-   Added `CHANGELOG.md`.
-   Added GitHub action workflow.
-   Removed `TravisCI` and `CircleCI`.
-   Removed some dead code.

## [0.3.7](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.3.7) - 2019-12-18
-   Added docstrings to methods.
-   Fixed tests import.
-   Updated requirements.
-   Added CircleCI workflow.

## [0.3.6](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.3.6) - 2019-11-15
-   Added python 3.8 official support.
-   Updated municipalities with data from ANPR.

## [0.3.5](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.3.5) - 2019-07-04
-   Updated requirements.
-   Improved code quality.

## [0.3.4](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.3.4) - 2019-02-07
-   Updated municipalities data.

## [0.3.3](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.3.3) - 2018-11-14
-   Fixed error on date - #3
-   Added python 3.7 to `tox` and `.travis`.

## [0.3.2](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.3.2) - 2018-09-17
-   Corrected some province names. #1
-   Replaced double unserscores with single ones. #2

## [0.3.1](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.3.1) - 2018-05-03
-   Updated requirements.

## [0.3.0](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.3.0) - 2017-11-06
-   Removed `omocodes` argument from `encode` method.

## [0.2.1](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.2.1) - 2017-10-18
-   Added raw values to decoded data.

## [0.2.0](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.2.0) - 2017-10-17
-   Improved omocodia support and added `is_omocode` method.

## [0.1.1](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.1.1) - 2017-10-12
-   Raised error if the birthplace is not mapped to a code.
-   Increased tests coverage.
-   Code refactoring.

## [0.1.0](https://github.com/fabiocaccamo/python-codicefiscale/releases/tag/0.1.0) - 2017-10-10
-   Released package on pypi.
