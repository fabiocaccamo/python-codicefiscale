import unittest

from codicefiscale import codicefiscale


class Issue0037TestCase(unittest.TestCase):
    def test_issue_0037(self):
        # when encoding a Codice Fiscale for a person born in Vignola (MO)
        # encode uses code L884 (for Vignola (TN) between 1920-1929) instead of L885.
        data = {
            "lastname": "Caccamo",
            "firstname": "Fabio",
            "gender": "M",
            "birthdate": "03/04/1885",
            "birthplace": "Vignola",
        }
        code = codicefiscale.encode(**data)
        data = codicefiscale.decode(code)
        birthplace = data["birthplace"]
        self.assertTrue(birthplace is not None)
        self.assertTrue(isinstance(birthplace, dict))
        # print(birthplace)
        self.assertEqual(birthplace["code"], "L885")
        self.assertEqual(birthplace["name"], "Vignola")
        self.assertEqual(birthplace["province"], "MO")
