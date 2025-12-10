import datetime

from codicefiscale import codicefiscale


def test_issue_0203():
    """
    Test for people over 100 years old.
    https://github.com/fabiocaccamo/python-codicefiscale/issues/203
    """
    code = codicefiscale.encode("Michele", "Faedi", "m", "01/01/1907", "Gallico")
    assert code == "MCHFDA07A01D877A"

    code_data = codicefiscale.decode(code)
    code_data.pop("omocodes", None)
    expected_code_data = {
        "code": "MCHFDA07A01D877A",
        "gender": "M",
        "birthdate": datetime.datetime(1907, 1, 1, 0, 0),
        "birthplace": {
            "active": False,
            "code": "D877",
            "date_created": "1861-03-17T00:00:00",
            "date_deleted": "1927-08-02T00:00:00",
            "name": "Gallico",
            "name_alt": "",
            "name_alt_trans": "",
            "name_slugs": ["gallico"],
            "name_trans": "Gallico",
            "province": "RC",
        },
        "raw": {
            "code": "MCHFDA07A01D877A",
            "lastname": "MCH",
            "firstname": "FDA",
            "birthdate": "07A01",
            "birthdate_year": "07",
            "birthdate_month": "A",
            "birthdate_day": "01",
            "birthplace": "D877",
            "cin": "A",
        },
    }
    assert code_data == expected_code_data
