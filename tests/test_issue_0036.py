import unittest

from codicefiscale import codicefiscale


class Issue0036TestCase(unittest.TestCase):
    def test_issue_0036(self):
        items = (
            ("CCCFBA85D03Z105P", "Cecoslovacchia"),
            ("CCCFBA85D03Z111D", "Repubblica Democratica Tedesca"),
            ("CCCFBA85D03Z118W", "Jugoslavia"),
            ("CCCFBA85D03Z135S", "Unione Repubbliche Socialiste Sovietiche"),
            ("CCCFBA05D03Z157G", "Serbia e Montenegro"),
            ("CCCFBA75D03Z201F", "Federazione dell'Arabia Meridionale"),
            ("CCCFBA75D03Z202K", "Protettorato dell'Arabia Meridionale"),
            ("CCCFBA85D03Z250N", "Yemen del Sud"),
        )
        for item in items:
            with self.subTest(item):
                code, expected_country = item
                data = codicefiscale.decode(code)
                self.assertEqual(data["birthplace"]["name"], expected_country)
