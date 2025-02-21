import pytest

from codicefiscale import codicefiscale

test_data = [
    ("CCCFBA85D03Z105P", "Cecoslovacchia"),
    ("CCCFBA85D03Z111D", "Repubblica Democratica Tedesca"),
    ("CCCFBA85D03Z118W", "Jugoslavia"),
    ("CCCFBA85D03Z135S", "Unione Repubbliche Socialiste Sovietiche"),
    ("CCCFBA05D03Z157G", "Serbia e Montenegro"),
    ("CCCFBA75D03Z201F", "Federazione dell'Arabia Meridionale"),
    ("CCCFBA75D03Z202K", "Protettorato dell'Arabia Meridionale"),
    ("CCCFBA85D03Z250N", "Yemen del Sud"),
]


@pytest.mark.parametrize("code, expected_country", test_data)
def test_issue_0036(code, expected_country):
    """
    Test for decoding fiscal codes with historical country names.
    """
    data = codicefiscale.decode(code)
    assert data["birthplace"]["name"] == expected_country
