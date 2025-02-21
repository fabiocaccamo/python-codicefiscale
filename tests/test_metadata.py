import re

from codicefiscale.metadata import (
    __author__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __version__,
)


def test_metadata():
    """
    Test that all metadata attributes are non-empty.
    """
    assert all(
        [
            __author__,
            __copyright__,
            __description__,
            __license__,
            __title__,
            __version__,
        ]
    )


def test_version():
    """
    Test that the version string follows the expected pattern (e.g., X.Y.Z).
    """
    version_pattern = re.compile(r"^(([\d]+)\.([\d]+)\.([\d]+))$")
    assert version_pattern.match(__version__)
