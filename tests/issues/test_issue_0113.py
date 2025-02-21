import datetime

import pytest

from codicefiscale import codicefiscale

test_data = [
    ("XXXXXX39D44G133O", datetime.datetime(1939, 4, 4, 0, 0)),
    ("XXXXXX46D11F383M", datetime.datetime(1946, 4, 11, 0, 0)),
    ("XXXXXX50H18F383N", datetime.datetime(1950, 6, 18, 0, 0)),
    ("XXXXXX38C71L513V", datetime.datetime(1938, 3, 31, 0, 0)),
    ("XXXXXX43C14G133F", datetime.datetime(1943, 3, 14, 0, 0)),
]


@pytest.mark.parametrize("code, expected_birthdate", test_data)
def test_issue_0113(code, expected_birthdate):
    """
    Test for wrong birthplace code error (missing date-range in the data-source).
    """
    code_data = codicefiscale.decode(code)
    code_data.pop("omocodes")
    code_data.pop("raw")
    assert code_data["birthdate"] == expected_birthdate
