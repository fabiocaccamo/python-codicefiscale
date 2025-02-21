from codicefiscale import codicefiscale


def test_issue_0037():
    """
    Test for encoding a Codice Fiscale for a person born in Vignola (MO).
    Ensures the correct birthplace code (L885) is used instead of L884.
    """
    data = {
        "lastname": "Caccamo",
        "firstname": "Fabio",
        "gender": "M",
        "birthdate": "03/04/1885",
        "birthplace": "Vignola",
    }
    code = codicefiscale.encode(**data)
    decoded_data = codicefiscale.decode(code)
    birthplace = decoded_data["birthplace"]
    assert birthplace is not None
    assert isinstance(birthplace, dict)
    assert birthplace["code"] == "L885"
    assert birthplace["name"] == "Vignola"
    assert birthplace["province"] == "MO"
