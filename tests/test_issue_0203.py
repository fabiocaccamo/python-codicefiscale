import unittest
from datetime import datetime, timedelta

from codicefiscale import codicefiscale


class Issue0203TestCase(unittest.TestCase):
    def test_issue_0203(self):
        """
        Encode a person in an old municipality (active = false)
        And the person is more than 100 years old
        """
        try:
            codicefiscale.encode('Mario', 'Rossi', 'm', datetime.now() - timedelta(days=150 * 365), 'Gallico')
        except ValueError as e:
            self.fail(f"codicefiscale.encode raised an exception: {e}")
