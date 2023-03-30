import unittest

from codicefiscale import codicefiscale


class Issue0016TestCase(unittest.TestCase):
    def test_issue_0016(self):
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
        self.assertEqual(birthplace["code"], expected_birthplace["code"])
        self.assertEqual(birthplace["name"].upper(), expected_birthplace["name"])
        self.assertEqual(birthplace["province"], expected_birthplace["province"])
