import datetime
import unittest

from codicefiscale import codicefiscale


class Issue0113TestCase(unittest.TestCase):
    def test_issue_0113(self):
        """
        Wrong birthplace code error (missing date-range in the data-source).
        """
        codes = [
            "XXXXXX39D44G133O",
            "XXXXXX46D11F383M",
            "XXXXXX50H18F383N",
            "XXXXXX38C71L513V",
            "XXXXXX43C14G133F",
        ]
        expected_birthdates = [
            datetime.datetime(1939, 4, 4, 0, 0),
            datetime.datetime(1946, 4, 11, 0, 0),
            datetime.datetime(1950, 6, 18, 0, 0),
            datetime.datetime(1938, 3, 31, 0, 0),
            datetime.datetime(1943, 3, 14, 0, 0),
        ]
        for index, code in enumerate(codes):
            with self.subTest(f"code: {code}"):
                code_data = codicefiscale.decode(code)
                code_data.pop("omocodes")
                code_data.pop("raw")
                # print(code_data)
                self.assertEqual(code_data["birthdate"], expected_birthdates[index])
