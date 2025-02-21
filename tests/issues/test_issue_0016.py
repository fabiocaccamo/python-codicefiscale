from codicefiscale import codicefiscale


def test_issue_0016():
    """
    Decode return GIRGENTI (soppresso) instead of AGRIGENTO
    """
    data = codicefiscale.decode("LNNFNC80A01A089K")
    expected_birthplace = {
        "code": "A089",
        "province": "AG",
        "name": "AGRIGENTO",
    }
    birthplace = data["birthplace"]
    assert birthplace["code"] == expected_birthplace["code"]
    assert birthplace["name"].upper() == expected_birthplace["name"]
    assert birthplace["province"] == expected_birthplace["province"]
