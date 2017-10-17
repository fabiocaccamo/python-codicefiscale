|Build Status| |codecov| |Code Health| |PyPI version| |Py versions| |License|

python-codicefiscale
====================

python-codicefiscale is a tiny library for encode/decode Italian fiscal
code - **codifica/decodifica del Codice Fiscale**.

Features
--------

-  **Transliteration** for name/surname
-  **Multiple** birthdate formats (datetime/string) *(you can see all the supported string formats in* ``tests/tests.py`` *)*
-  **Automatic** birthplace city/foreign-country code detection from name
-  **Omocodia** support

Installation
------------

``pip install python-codicefiscale``

Usage
-----

Import
^^^^^^

.. code:: python

    from codicefiscale import codicefiscale

Encode
^^^^^^

.. code:: python

    codicefiscale.encode(surname='Caccamo', name='Fabio', sex='M', birthdate='03/04/1985', birthplace='Torino')

    # 'CCCFBA85D03L219P'

Decode
^^^^^^

.. code:: python

    codicefiscale.decode('CCCFBA85D03L219P')

    # {
    #     'surname': 'CCC',
    #     'name': 'FBA',
    #     'sex': 'M',
    #     'birthdate': datetime.datetime(1985, 4, 3, 0, 0),
    #     'birthplace': {
    #         'province': 'TO',
    #         'code': 'L219',
    #         'name': 'TORINO'
    #     },
    #     'cin': 'P',
    #     'code': 'CCCFBA85D03L219P',
    #     'omocodes': [
    #         'CCCFBA85D03L219P',
    #         'CCCFBA85D03L21VE',
    #         'CCCFBA85D03L2MVP',
    #         'CCCFBA85D03LNMVE',
    #         'CCCFBA85D0PLNMVA',
    #         'CCCFBA85DLPLNMVL',
    #         'CCCFBA8RDLPLNMVX',
    #         'CCCFBAURDLPLNMVU'
    #     ],
    # }

Check
^^^^^

.. code:: python

    codicefiscale.is_valid('CCCFBA85D03L219P')

    # True

.. code:: python

    codicefiscale.is_omocode('CCCFBA85D03L219P')

    # False

.. code:: python

    codicefiscale.is_omocode('CCCFBA85D03L21VE')

    # True

Test
~~~~

``tox`` / ``python setup.py test`` / ``python -m unittest tests.tests``

--------------

License
-------

Released under `MIT License`_.

.. _MIT License: LICENSE

.. |Build Status| image:: https://travis-ci.org/fabiocaccamo/python-codicefiscale.svg?branch=master
.. |codecov| image:: https://codecov.io/gh/fabiocaccamo/python-codicefiscale/branch/master/graph/badge.svg
.. |Code Health| image:: https://landscape.io/github/fabiocaccamo/python-codicefiscale/master/landscape.svg?style=flat
.. |PyPI version| image:: https://badge.fury.io/py/python-codicefiscale.svg
.. |Py versions| image:: https://img.shields.io/pypi/pyversions/python-codicefiscale.svg
.. |License| image:: https://img.shields.io/pypi/l/python-codicefiscale.svg