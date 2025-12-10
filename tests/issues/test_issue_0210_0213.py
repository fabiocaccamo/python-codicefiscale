import datetime

from codicefiscale import codicefiscale


def test_issue_0210():
    """
    Test for municipality activated after birthdate.
    https://github.com/fabiocaccamo/python-codicefiscale/issues/210
    """
    code = "CCCFBA30H66F991T"
    assert codicefiscale.is_valid(code)
    code_data = codicefiscale.decode(code)
    code_data.pop("omocodes")
    expected_code_data = {
        "code": "CCCFBA30H66F991T",
        "gender": "F",
        "birthdate": datetime.datetime(1930, 6, 26, 0, 0),
        "birthplace": {
            "active": False,
            "code": "F991",
            "date_created": "1958-01-26T00:00:00",
            "date_deleted": "1965-01-07T00:00:00",
            "name": "Nuxis",
            "name_alt": "",
            "name_alt_trans": "",
            "name_slugs": ["nuxis"],
            "name_trans": "Nuxis",
            "province": "CA",
        },
        "raw": {
            "code": "CCCFBA30H66F991T",
            "lastname": "CCC",
            "firstname": "FBA",
            "birthdate": "30H66",
            "birthdate_year": "30",
            "birthdate_month": "H",
            "birthdate_day": "66",
            "birthplace": "F991",
            "cin": "T",
        },
    }
    assert code_data == expected_code_data


def test_issue_0213():
    """
    Test for municipality activated after birthdate.
    https://github.com/fabiocaccamo/python-codicefiscale/issues/213
    """
    code = "DBRGRZ53R66F059C"
    assert codicefiscale.is_valid(code)
    code_data = codicefiscale.decode(code)
    code_data.pop("omocodes")
    expected_code_data = {
        "code": "DBRGRZ53R66F059C",
        "gender": "F",
        "birthdate": datetime.datetime(1953, 10, 26, 0, 0),
        "birthplace": {
            "active": True,
            "code": "F059",
            "date_created": "1955-08-19T00:00:00",
            "date_deleted": "",
            "name": "Mattinata",
            "name_alt": "",
            "name_alt_trans": "",
            "name_slugs": ["mattinata"],
            "name_trans": "Mattinata",
            "province": "FG",
        },
        "raw": {
            "code": "DBRGRZ53R66F059C",
            "lastname": "DBR",
            "firstname": "GRZ",
            "birthdate": "53R66",
            "birthdate_year": "53",
            "birthdate_month": "R",
            "birthdate_day": "66",
            "birthplace": "F059",
            "cin": "C",
        },
    }
    assert code_data == expected_code_data
