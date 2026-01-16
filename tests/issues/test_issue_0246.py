import datetime

from codicefiscale import codicefiscale


def test_issue_0246():
    """
    Test problem with municipalities that have the same or similar name
    that once slugified return the same string: e.g., Paternò (CT) vs Paterno (PZ)
    https://github.com/fabiocaccamo/python-codicefiscale/issues/246
    """

    code = codicefiscale.encode(
        lastname="DE GREGORI",
        firstname="FRANCESCO",
        gender="M",
        birthdate="31/12/1984",
        birthplace="PATERNÒ",
    )
    assert code == "DGRFNC84T31G371E"

    code_data = codicefiscale.decode(code)
    code_data.pop("omocodes", None)
    expected_code_data = {
        "code": "DGRFNC84T31G371E",
        "gender": "M",
        "birthdate": datetime.datetime(1984, 12, 31, 0, 0),
        "birthplace": {
            "active": False,
            "code": "G371",
            "date_created": "1861-03-17T00:00:00",
            "date_deleted": "1985-05-16T00:00:00",
            "name": "Paternò",
            "name_alt": "",
            "name_alt_trans": "",
            "name_slugs": ["paterno"],
            "name_trans": "Paterno'",
            "province": "CT",
        },
        "raw": {
            "code": "DGRFNC84T31G371E",
            "lastname": "DGR",
            "firstname": "FNC",
            "birthdate": "84T31",
            "birthdate_year": "84",
            "birthdate_month": "T",
            "birthdate_day": "31",
            "birthplace": "G371",
            "cin": "E",
        },
    }
    assert code_data == expected_code_data
