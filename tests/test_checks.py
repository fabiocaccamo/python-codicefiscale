import pytest

from codicefiscale import codicefiscale


@pytest.fixture
def omocode_test_cases():
    return [
        ("CCCFBA85D03L219P", False),
        ("CCCFBA85D03L21VE", True),
        ("CCCFBA85D03L2MVP", True),
        ("CCCFBA85D03LNMVE", True),
        ("CCCFBA85D0PLNMVA", True),
        ("CCCFBA85DLPLNMVL", True),
        ("CCCFBA8RDLPLNMVX", True),
        ("CCCFBAURDLPLNMVU", True),
    ]


@pytest.fixture
def valid_fiscal_code_test_cases():
    return [
        ("CCCFBA85D03L219P", True),
        ("CCC FBA 85 D03 L219 P", True),
        ("CCC-FBA-85-D03-L219-P", True),
        ("CCCFBA85D03L219PP", False),  # too long
        ("CCCFBA85D03L219B", False),  # wrong CIN
        ("CCCFBA85D03L219", False),  # too short
        ("CCCFBA85D00L219", False),  # wrong birthdate day
        ("CCCFBA85D99L219", False),  # wrong birthdate day
    ]


def test_is_omocode(omocode_test_cases):
    """
    Test the `is_omocode` function to verify if a fiscal code is an omocode.
    """
    for fiscal_code, expected_result in omocode_test_cases:
        assert codicefiscale.is_omocode(fiscal_code) == expected_result


def test_is_valid(valid_fiscal_code_test_cases):
    """
    Test the `is_valid` function to verify if a fiscal code is valid.
    """
    for fiscal_code, expected_result in valid_fiscal_code_test_cases:
        assert codicefiscale.is_valid(fiscal_code) == expected_result
