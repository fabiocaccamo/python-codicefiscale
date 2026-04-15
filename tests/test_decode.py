from datetime import datetime

import pytest

from codicefiscale import codicefiscale


@pytest.fixture
def decode_test_cases():
    return [
        {
            "input": "THDSDA95P08Z330H",
            "result": {
                "gender": "M",
                "birthdate": "08/09/1995",
                "birthplace": "Marocco",
            },
        },
        {
            "input": "BLSLGS84C22Z145O",
            "result": {
                "gender": "M",
                "birthdate": "22/03/1984",
                "birthplace": "Lettonia",
            },
        },
        {
            "input": "BRNGNN71B26L219T",
            "result": {
                "gender": "M",
                "birthdate": "26/02/1971",
                "birthplace": "Torino",
            },
        },
        {
            "input": "CCCFBA85D03L219P",
            "result": {
                "gender": "M",
                "birthdate": "03/04/1985",
                "birthplace": "Torino",
            },
        },
        {
            "input": "GMBLSN84A05G674H",
            "result": {
                "gender": "M",
                "birthdate": "05/01/1984",
                "birthplace": "Pinerolo",
            },
        },
        {
            "input": "MRTMRA83T56A269B",
            "result": {
                "gender": "F",
                "birthdate": "16/12/1983",
                "birthplace": "Anagni",
            },
        },
        {
            "input": "PNLMHL79R27I158P",
            "result": {
                "gender": "M",
                "birthdate": "27/10/1979",
                "birthplace": "San Severo",
            },
        },
        {
            "input": "QTRDRA71P13G388J",
            "result": {
                "gender": "M",
                "birthdate": "13/09/1971",
                "birthplace": "Pavia",
            },
        },
        {
            "input": "TKKYKU87B68L219F",
            "result": {
                "gender": "F",
                "birthdate": "28/02/1987",
                "birthplace": "Torino",
            },
        },
        {
            "input": "RSSMRA68A01H501Y",
            "result": {
                "gender": "M",
                "birthdate": "01/01/1968",
                "birthplace": "Roma",
            },
        },
        {
            "input": "RSSMRA50B17A558W",
            "result": {
                "gender": "M",
                "birthdate": "17/02/1950",
                "birthplace": "Porretta Terme",
            },
        },
    ]


@pytest.fixture
def decode_omocodia_test_cases():
    return [
        {
            "input": "CCCFBA85D03L219P",
            "result": {
                "gender": "M",
                "birthdate": "03/04/1985",
                "birthplace": "Torino",
            },
        },
        {
            "input": "CCCFBA85D03L21VE",
            "result": {
                "gender": "M",
                "birthdate": "03/04/1985",
                "birthplace": "Torino",
            },
        },
        {
            "input": "CCCFBA85D03L2MVP",
            "result": {
                "gender": "M",
                "birthdate": "03/04/1985",
                "birthplace": "Torino",
            },
        },
        {
            "input": "CCCFBA85D03LNMVE",
            "result": {
                "gender": "M",
                "birthdate": "03/04/1985",
                "birthplace": "Torino",
            },
        },
        {
            "input": "CCCFBA85D0PLNMVA",
            "result": {
                "gender": "M",
                "birthdate": "03/04/1985",
                "birthplace": "Torino",
            },
        },
        {
            "input": "CCCFBA85DLPLNMVL",
            "result": {
                "gender": "M",
                "birthdate": "03/04/1985",
                "birthplace": "Torino",
            },
        },
        {
            "input": "CCCFBA8RDLPLNMVX",
            "result": {
                "gender": "M",
                "birthdate": "03/04/1985",
                "birthplace": "Torino",
            },
        },
        {
            "input": "CCCFBAURDLPLNMVU",
            "result": {
                "gender": "M",
                "birthdate": "03/04/1985",
                "birthplace": "Torino",
            },
        },
    ]


@pytest.fixture
def decode_omocodes_test_case():
    return {
        "input": "CCCFBA85D03L219P",
        "expected_omocodes": [
            "CCCFBA85D03L219P",
            "CCCFBA85D03L21VE",
            "CCCFBA85D03L2M9A",
            "CCCFBA85D03LN19E",
            "CCCFBA85D0PL219L",
            "CCCFBA85DL3L219A",
            "CCCFBA8RD03L219B",
            "CCCFBAU5D03L219M",
            "CCCFBA85D03L2MVP",
            "CCCFBA85D03LN1VT",
            "CCCFBA85D0PL21VA",
            "CCCFBA85DL3L21VP",
            "CCCFBA8RD03L21VQ",
            "CCCFBAU5D03L21VB",
            "CCCFBA85D03LNM9P",
            "CCCFBA85D0PL2M9W",
            "CCCFBA85DL3L2M9L",
            "CCCFBA8RD03L2M9M",
            "CCCFBAU5D03L2M9X",
            "CCCFBA85D0PLN19A",
            "CCCFBA85DL3LN19P",
            "CCCFBA8RD03LN19Q",
            "CCCFBAU5D03LN19B",
            "CCCFBA85DLPL219W",
            "CCCFBA8RD0PL219X",
            "CCCFBAU5D0PL219I",
            "CCCFBA8RDL3L219M",
            "CCCFBAU5DL3L219X",
            "CCCFBAURD03L219Y",
            "CCCFBA85D03LNMVE",
            "CCCFBA85D0PL2MVL",
            "CCCFBA85DL3L2MVA",
            "CCCFBA8RD03L2MVB",
            "CCCFBAU5D03L2MVM",
            "CCCFBA85D0PLN1VP",
            "CCCFBA85DL3LN1VE",
            "CCCFBA8RD03LN1VF",
            "CCCFBAU5D03LN1VQ",
            "CCCFBA85DLPL21VL",
            "CCCFBA8RD0PL21VM",
            "CCCFBAU5D0PL21VX",
            "CCCFBA8RDL3L21VB",
            "CCCFBAU5DL3L21VM",
            "CCCFBAURD03L21VN",
            "CCCFBA85D0PLNM9L",
            "CCCFBA85DL3LNM9A",
            "CCCFBA8RD03LNM9B",
            "CCCFBAU5D03LNM9M",
            "CCCFBA85DLPL2M9H",
            "CCCFBA8RD0PL2M9I",
            "CCCFBAU5D0PL2M9T",
            "CCCFBA8RDL3L2M9X",
            "CCCFBAU5DL3L2M9I",
            "CCCFBAURD03L2M9J",
            "CCCFBA85DLPLN19L",
            "CCCFBA8RD0PLN19M",
            "CCCFBAU5D0PLN19X",
            "CCCFBA8RDL3LN19B",
            "CCCFBAU5DL3LN19M",
            "CCCFBAURD03LN19N",
            "CCCFBA8RDLPL219I",
            "CCCFBAU5DLPL219T",
            "CCCFBAURD0PL219U",
            "CCCFBAURDL3L219J",
            "CCCFBA85D0PLNMVA",
            "CCCFBA85DL3LNMVP",
            "CCCFBA8RD03LNMVQ",
            "CCCFBAU5D03LNMVB",
            "CCCFBA85DLPL2MVW",
            "CCCFBA8RD0PL2MVX",
            "CCCFBAU5D0PL2MVI",
            "CCCFBA8RDL3L2MVM",
            "CCCFBAU5DL3L2MVX",
            "CCCFBAURD03L2MVY",
            "CCCFBA85DLPLN1VA",
            "CCCFBA8RD0PLN1VB",
            "CCCFBAU5D0PLN1VM",
            "CCCFBA8RDL3LN1VQ",
            "CCCFBAU5DL3LN1VB",
            "CCCFBAURD03LN1VC",
            "CCCFBA8RDLPL21VX",
            "CCCFBAU5DLPL21VI",
            "CCCFBAURD0PL21VJ",
            "CCCFBAURDL3L21VY",
            "CCCFBA85DLPLNM9W",
            "CCCFBA8RD0PLNM9X",
            "CCCFBAU5D0PLNM9I",
            "CCCFBA8RDL3LNM9M",
            "CCCFBAU5DL3LNM9X",
            "CCCFBAURD03LNM9Y",
            "CCCFBA8RDLPL2M9T",
            "CCCFBAU5DLPL2M9E",
            "CCCFBAURD0PL2M9F",
            "CCCFBAURDL3L2M9U",
            "CCCFBA8RDLPLN19X",
            "CCCFBAU5DLPLN19I",
            "CCCFBAURD0PLN19J",
            "CCCFBAURDL3LN19Y",
            "CCCFBAURDLPL219F",
            "CCCFBA85DLPLNMVL",
            "CCCFBA8RD0PLNMVM",
            "CCCFBAU5D0PLNMVX",
            "CCCFBA8RDL3LNMVB",
            "CCCFBAU5DL3LNMVM",
            "CCCFBAURD03LNMVN",
            "CCCFBA8RDLPL2MVI",
            "CCCFBAU5DLPL2MVT",
            "CCCFBAURD0PL2MVU",
            "CCCFBAURDL3L2MVJ",
            "CCCFBA8RDLPLN1VM",
            "CCCFBAU5DLPLN1VX",
            "CCCFBAURD0PLN1VY",
            "CCCFBAURDL3LN1VN",
            "CCCFBAURDLPL21VU",
            "CCCFBA8RDLPLNM9I",
            "CCCFBAU5DLPLNM9T",
            "CCCFBAURD0PLNM9U",
            "CCCFBAURDL3LNM9J",
            "CCCFBAURDLPL2M9Q",
            "CCCFBAURDLPLN19U",
            "CCCFBA8RDLPLNMVX",
            "CCCFBAU5DLPLNMVI",
            "CCCFBAURD0PLNMVJ",
            "CCCFBAURDL3LNMVY",
            "CCCFBAURDLPL2MVF",
            "CCCFBAURDLPLN1VJ",
            "CCCFBAURDLPLNM9F",
            "CCCFBAURDLPLNMVU",
        ],
    }


def test_decode(decode_test_cases):
    """Test decoding fiscal codes."""
    for case in decode_test_cases:
        result = case["result"]
        decoded = codicefiscale.decode(case["input"])

        # check gender
        gender = decoded.get("gender")
        assert gender is not None, "Gender should not be None"
        assert gender == result["gender"], f"Gender mismatch for {case['input']}"

        # check birthdate
        birthdate = decoded.get("birthdate")
        assert birthdate is not None, "Birthdate should not be None"
        assert birthdate == datetime.strptime(result["birthdate"], "%d/%m/%Y"), (
            f"Birthdate mismatch for {case['input']}"
        )

        # check birthplace
        birthplace = decoded.get("birthplace")
        assert birthplace is not None, "Birthplace should not be None"
        assert birthplace["name"].upper() == result["birthplace"].upper(), (
            f"Birthplace mismatch for {case['input']}"
        )


def test_decode_invalid_syntax():
    """Test decoding with invalid syntax."""
    with pytest.raises(ValueError):
        codicefiscale.decode("CC0FBA85X03L219P")  # invalid lastname
    with pytest.raises(ValueError):
        codicefiscale.decode("CCCFB085X03L219P")  # invalid firstname
    with pytest.raises(ValueError):
        codicefiscale.decode("CCCFBA8XD03L219S")  # invalid date-year
    with pytest.raises(ValueError):
        codicefiscale.decode("CCCFBA85X03L219P")  # invalid date-month
    with pytest.raises(ValueError):
        codicefiscale.decode("CCCFBA85D00L219P")  # invalid date-day


def test_decode_omocodia(decode_omocodia_test_cases):
    """Test decoding fiscal codes with omocodia."""
    for case in decode_omocodia_test_cases:
        result = case["result"]
        decoded = codicefiscale.decode(case["input"])

        # check gender
        gender = decoded.get("gender")
        assert gender is not None, "Gender should not be None"
        assert gender == result["gender"], f"Gender mismatch for {case['input']}"

        # check birthdate
        birthdate = decoded.get("birthdate")
        assert birthdate is not None, "Birthdate should not be None"
        assert birthdate == datetime.strptime(result["birthdate"], "%d/%m/%Y"), (
            f"Birthdate mismatch for {case['input']}"
        )

        # check birthplace
        birthplace = decoded.get("birthplace")
        assert birthplace is not None, "Birthplace should not be None"
        assert birthplace["name"].upper() == result["birthplace"].upper(), (
            f"Birthplace mismatch for {case['input']}"
        )

        # check omocodes
        omocodes = decoded.get("omocodes", [])
        assert len(omocodes) == 128, f"Expected 128 omocodes for {case['input']}"


def test_decode_omocodes(decode_omocodes_test_case):
    """Test decoding fiscal codes and verifying omocodes."""
    decoded = codicefiscale.decode(decode_omocodes_test_case["input"])
    assert len(decoded["omocodes"]) == 128, "Expected 128 omocodes"
    assert decoded["omocodes"] == decode_omocodes_test_case["expected_omocodes"], (
        "Omocodes mismatch"
    )


def test_decode_with_invalid_birthplace():
    """Test decoding with an invalid birthplace."""
    code = "FRTMXM74L15D354A"
    valid = codicefiscale.is_valid(code)
    assert not valid, "Expected invalid fiscal code"


def test_decode_firstname_options():
    """Test decoding fiscal code with firstname_options verification."""
    code = "CCCFBA85D03L219P"
    decoded = codicefiscale.decode(code)

    firstname_options = decoded.get("firstname_options")
    assert firstname_options is not None
    assert "Fabio" in firstname_options


def test_decode_firstname_options_foreign_birthplace():
    """Test that firstname_options is empty for foreign birthplaces."""
    # foreign birthplace (Marocco - Z330)
    foreign_code = "THDSDA95P08Z330H"
    foreign_decoded = codicefiscale.decode(foreign_code)

    assert "firstname_options" in foreign_decoded
    assert foreign_decoded["firstname_options"] == []

    # italian birthplace (Torino - L219)
    italian_code = "CCCFBA85D03L219P"
    italian_decoded = codicefiscale.decode(italian_code)

    assert "firstname_options" in italian_decoded
    assert len(italian_decoded["firstname_options"]) > 0
    assert isinstance(italian_decoded["firstname_options"], list)


def test_decode_firstname():
    """Test decode_firstname function with different parameters."""
    # test with gender M
    names_m = codicefiscale.decode_firstname("FBA", "M")
    assert names_m is not None
    assert isinstance(names_m, list)
    assert "Fabio" in names_m

    # test with gender F
    names_f = codicefiscale.decode_firstname("FBA", "F")
    assert names_f is not None
    assert isinstance(names_f, list)
    assert "Fabia" in names_f or "Fabiana" in names_f

    # test without gender (should return both M and F, deduplicated)
    names_all = codicefiscale.decode_firstname("FBA")
    assert names_all is not None
    assert isinstance(names_all, list)
    assert len(names_all) == len(set(names_all))  # no duplicates
    assert len(names_all) >= max(len(names_m), len(names_f))

    # test unisex name (Alex) - should appear only once
    names_alex = codicefiscale.decode_firstname("LXA")
    assert names_alex is not None
    assert len(names_alex) == len(set(names_alex))  # no duplicates
    assert names_alex.count("Alex") == 1

    # test with invalid code
    names_invalid = codicefiscale.decode_firstname("XXX")
    assert names_invalid is None
