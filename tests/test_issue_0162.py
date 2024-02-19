import datetime
import unittest

from codicefiscale import codicefiscale


class Issue0162TestCase(unittest.TestCase):
    def test_issue_0162(self):
        """
        Wrong birthplace code error (missing date-range in the data-source).
        """
        self.maxDiff = None
        code = "DFLNTN42T20B860H"
        self.assertTrue(codicefiscale.is_valid(code))
        code_data = codicefiscale.decode(code)
        code_data.pop("omocodes")
        # print(code_data)
        expected_code_data = {
            "code": "DFLNTN42T20B860H",
            "gender": "M",
            "birthdate": datetime.datetime(1942, 12, 20, 0, 0),
            "birthplace": {
                "active": False,
                "code": "B860",
                "date_created": "1927-01-12T00:00:00",
                "date_deleted": "1928-06-27T00:00:00",
                "name": "Casagiove",
                "name_alt": "",
                "name_alt_trans": "",
                "name_slugs": ["casagiove"],
                "name_trans": "Casagiove",
                "province": "NA",
            },
            "raw": {
                "code": "DFLNTN42T20B860H",
                "lastname": "DFL",
                "firstname": "NTN",
                "birthdate": "42T20",
                "birthdate_year": "42",
                "birthdate_month": "T",
                "birthdate_day": "20",
                "birthplace": "B860",
                "cin": "H",
            },
        }
        self.assertEqual(code_data, expected_code_data)
