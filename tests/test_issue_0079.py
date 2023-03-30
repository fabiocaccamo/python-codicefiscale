import datetime
import unittest

from codicefiscale import codicefiscale


class Issue0079TestCase(unittest.TestCase):
    def test_issue_0079(self):
        """
        Unable to encode and decode fiscal codes
        when year of birth (excluding century) < 10 (eg. 2004).
        """

        code = codicefiscale.encode(
            lastname="Rossi",
            firstname="Mario",
            gender="M",
            birthdate="29/11/2004",
            birthplace="Torino",
        )
        self.assertEqual(code, "RSSMRA04S29L219G")

        code_data = codicefiscale.decode("RSSMRA00S29L219C")
        code_data.pop("omocodes")
        expected_code_data = {
            "code": "RSSMRA00S29L219C",
            "gender": "M",
            "birthdate": datetime.datetime(2000, 11, 29, 0, 0),
            "birthplace": {
                "active": True,
                "code": "L219",
                "date_created": "1889-08-12T00:00:00",
                "date_deleted": "",
                "name": "Torino",
                "name_alt": "",
                "name_alt_trans": "",
                "name_slugs": ["torino"],
                "name_trans": "Torino",
                "province": "TO",
            },
            "raw": {
                "code": "RSSMRA00S29L219C",
                "lastname": "RSS",
                "firstname": "MRA",
                "birthdate": "00S29",
                "birthdate_year": "00",
                "birthdate_month": "S",
                "birthdate_day": "29",
                "birthplace": "L219",
                "cin": "C",
            },
        }
        self.assertEqual(code_data, expected_code_data)
