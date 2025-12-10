from datetime import datetime

import pytest

from codicefiscale import codicefiscale


@pytest.fixture
def lastname_test_cases():
    return [
        {"input": "", "result": "XXX"},
        {"input": "Caccamo", "result": "CCC"},
        {"input": "Fò", "result": "FOX"},
    ]


@pytest.fixture
def firstname_test_cases():
    return [
        {"input": "", "result": "XXX"},
        {"input": "Alessandro", "result": "LSN"},
        {"input": "Dario", "result": "DRA"},
        {"input": "Fabio", "result": "FBA"},
        {"input": "Giovanni", "result": "GNN"},
        {"input": "Hu", "result": "HUX"},
        {"input": "Maria", "result": "MRA"},
        {"input": "Michele", "result": "MHL"},
    ]


@pytest.fixture
def birthdate_formats_test_cases():
    return [
        {"input": datetime(1985, 4, 3), "result": "85D03"},
        {"input": "03 04 1985", "result": "85D03"},
        {"input": "03/04/1985", "result": "85D03"},
        {"input": "03-04-1985", "result": "85D03"},
        {"input": "03.04.1985", "result": "85D03"},
        {"input": "3/4/1985", "result": "85D03"},
        {"input": "3-4-1985", "result": "85D03"},
        {"input": "3.4.1985", "result": "85D03"},
        {"input": "1985 04 03", "result": "85D03"},
        {"input": "1985/04/03", "result": "85D03"},
        {"input": "1985-04-03", "result": "85D03"},
        {"input": "1985.04.03", "result": "85D03"},
        {"input": "1985/4/3", "result": "85D03"},
        {"input": "1985-4-3", "result": "85D03"},
        {"input": "1985.4.3", "result": "85D03"},
    ]


@pytest.fixture
def birthdate_gender_test_cases():
    return [
        {"input": ["03/04/1985", "M"], "result": "85D03"},
        {"input": ["03/04/1985", "F"], "result": "85D43"},
    ]


@pytest.fixture
def birthplace_italy_test_cases():
    return [
        {"input": "Torino, Italy", "result": "L219"},
        {"input": "Torino (TO), Italy", "result": "L219"},
        {"input": "Torino (TO)", "result": "L219"},
        {"input": "Torino", "result": "L219"},
        {"input": "L219", "result": "L219"},
    ]


@pytest.fixture
def birthplace_foreign_test_cases():
    return [
        {"input": "Lettonia", "result": "Z145"},
        {"input": "Giappone", "result": "Z219"},
        {"input": "Marocco", "result": "Z330"},
    ]


@pytest.fixture
def cin_test_cases():
    return [
        {"input": "CCCFBA85D03L219", "result": "P"},
    ]


@pytest.fixture
def encode_test_cases():
    return [
        {
            "input": {
                "lastname": "Ait Hadda",
                "firstname": "Saad",
                "gender": "M",
                "birthdate": "08/09/1995",
                "birthplace": "Marocco",
            },
            "result": "THDSDA95P08Z330H",
        },
        {
            "input": {
                "lastname": "Belousovs",
                "firstname": "Olegs",
                "gender": "M",
                "birthdate": "22/03/1984",
                "birthplace": "Lettonia",
            },
            "result": "BLSLGS84C22Z145O",
        },
        {
            "input": {
                "lastname": "Bruno",
                "firstname": "Giovanni",
                "gender": "M",
                "birthdate": "26/02/1971",
                "birthplace": "Torino",
            },
            "result": "BRNGNN71B26L219T",
        },
        {
            "input": {
                "lastname": "Caccamo",
                "firstname": "Fabio",
                "gender": "M",
                "birthdate": "03/04/1985",
                "birthplace": "Torino",
            },
            "result": "CCCFBA85D03L219P",
        },
        {
            "input": {
                "lastname": "Gomba",
                "firstname": "Alessandro",
                "gender": "M",
                "birthdate": "05/01/1984",
                "birthplace": "Pinerolo",
            },
            "result": "GMBLSN84A05G674H",
        },
        {
            "input": {
                "lastname": "Martini",
                "firstname": "Maria",
                "gender": "F",
                "birthdate": "16/12/1983",
                "birthplace": "Anagni",
            },
            "result": "MRTMRA83T56A269B",
        },
        {
            "input": {
                "lastname": "Panella",
                "firstname": "Michele",
                "gender": "M",
                "birthdate": "27/10/1979",
                "birthplace": "San Severo (FG)",
            },
            "result": "PNLMHL79R27I158P",
        },
        {
            "input": {
                "lastname": "Quatrini",
                "firstname": "Dario",
                "gender": "M",
                "birthdate": "13/09/1971",
                "birthplace": "Pavia",
            },
            "result": "QTRDRA71P13G388J",
        },
        {
            "input": {
                "lastname": "Takakura",
                "firstname": "Yuuki",
                "gender": "F",
                "birthdate": "28/02/1987",
                "birthplace": "Torino",
            },
            "result": "TKKYKU87B68L219F",
        },
        {
            "input": {
                "lastname": "Rossi",
                "firstname": "Mario",
                "gender": "M",
                "birthdate": "17/02/1950",
                "birthplace": "Porretta Terme",
            },
            "result": "RSSMRA50B17A558W",
        },
    ]


def test_encode_lastname(lastname_test_cases):
    """Test encoding last names."""
    for case in lastname_test_cases:
        assert codicefiscale.encode_lastname(case["input"]) == case["result"]


def test_encode_firstname(firstname_test_cases):
    """Test encoding first names."""
    for case in firstname_test_cases:
        assert codicefiscale.encode_firstname(case["input"]) == case["result"]


def test_encode_birthdate_formats(birthdate_formats_test_cases):
    """Test encoding birthdates with various formats."""
    for case in birthdate_formats_test_cases:
        assert codicefiscale.encode_birthdate(case["input"], "M") == case["result"]


def test_encode_birthdate_invalid_arguments():
    """Test invalid arguments for encoding birthdates."""
    with pytest.raises(ValueError):
        codicefiscale.encode_birthdate(None, "M")
    with pytest.raises(ValueError):
        codicefiscale.encode_birthdate("03/04/1985", None)
    with pytest.raises(ValueError):
        codicefiscale.encode_birthdate("03/04/1985", "X")
    with pytest.raises(ValueError):
        codicefiscale.encode_birthdate("1985/1985/1985", "M")


def test_encode_birthdate_gender(birthdate_gender_test_cases):
    """Test encoding birthdates with gender."""
    for case in birthdate_gender_test_cases:
        assert codicefiscale.encode_birthdate(*case["input"]) == case["result"]


def test_encode_birthplace_italy(birthplace_italy_test_cases):
    """Test encoding birthplaces in Italy."""
    for case in birthplace_italy_test_cases:
        assert codicefiscale.encode_birthplace(case["input"]) == case["result"]


def test_encode_birthplace_foreign(birthplace_foreign_test_cases):
    """Test encoding birthplaces in foreign countries."""
    for case in birthplace_foreign_test_cases:
        assert codicefiscale.encode_birthplace(case["input"]) == case["result"]


def test_encode_birthplace_invalid_arguments():
    """Test invalid arguments for encoding birthplaces."""
    with pytest.raises(ValueError):
        codicefiscale.encode_birthplace(None)
    with pytest.raises(ValueError):
        codicefiscale.encode_birthplace("Area 51")


def test_encode_birthplace_created_after_birthdate():
    """Test encoding birthplace created after birthdate."""
    result = codicefiscale.encode_birthplace("Torino", "01/01/1888")
    assert result == "L219"


def test_encode_cin(cin_test_cases):
    """Test encoding CIN."""
    for case in cin_test_cases:
        assert codicefiscale.encode_cin(case["input"]) == case["result"]


def test_encode_cin_invalid_arguments():
    """Test invalid arguments for encoding CIN."""
    with pytest.raises(ValueError):
        codicefiscale.encode_cin(None)
    with pytest.raises(ValueError):
        codicefiscale.encode_cin("CCCFBA85D03")


def test_encode(encode_test_cases):
    """Test encoding full fiscal codes."""
    for case in encode_test_cases:
        assert codicefiscale.encode(**case["input"]) == case["result"]
