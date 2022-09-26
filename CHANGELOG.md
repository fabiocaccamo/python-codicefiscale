# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
