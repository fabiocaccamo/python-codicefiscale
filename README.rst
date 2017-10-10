|Build Status| |codecov| |Code Health| |PyPI version| |Py versions| |License|

python-codicefiscale
====================

python-codicefiscale is a tiny library for encode/decode Italian fiscal
code - **codifica/decodifica del Codice Fiscale**.

Features
--------

-  **Transliteration** for name/surname
-  **Multiple** birthdate formats (datetime/string) *(you can see all
   the supported string formats in tests/tests.py)*
-  **Automatic** birthplace city/country code detection
-  **Omocodia** support

Installation
------------

``pip install python-codicefiscale``

Usage
-----

Encoding
^^^^^^^^

.. code:: python

    from codicefiscale import codicefiscale

    codicefiscale.encode(surname='Caccamo', name='Fabio', sex='M', birthdate='03/04/1985', birthplace='Torino')

    # returns 'CCCFBA85D03L219P'

Decoding
^^^^^^^^

.. code:: python

    from codicefiscale import codicefiscale

    codicefiscale.decode('CCCFBA85D03L219P')

    # returns a dict contaning: 'code', 'sex' ('M' or 'F'), 'birthdate' (datetime), 'birthplace' (dict), 'cin'

Checking
^^^^^^^^

.. code:: python

    from codicefiscale import codicefiscale

    codicefiscale.is_valid('CCCFBA85D03L219P')

    # returns True

Testing
^^^^^^^

.. code:: python

    python -m unittest tests.tests
    # or
    python setup.py test
    # or
    tox

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