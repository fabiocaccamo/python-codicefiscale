from __future__ import annotations

import re
import string
from datetime import datetime, timedelta
from itertools import combinations
from re import Pattern
from typing import Any, Literal

from dateutil import parser as date_parser
from slugify import slugify

from codicefiscale.data import get_indexed_data

_CONSONANTS: list[str] = list("bcdfghjklmnpqrstvwxyz")
_VOWELS: list[str] = list("aeiou")
_MONTHS: list[str] = list("ABCDEHLMPRST")
_CIN: dict[str, tuple[int, int]] = {
    "0": (0, 1),
    "1": (1, 0),
    "2": (2, 5),
    "3": (3, 7),
    "4": (4, 9),
    "5": (5, 13),
    "6": (6, 15),
    "7": (7, 17),
    "8": (8, 19),
    "9": (9, 21),
    "A": (0, 1),
    "B": (1, 0),
    "C": (2, 5),
    "D": (3, 7),
    "E": (4, 9),
    "F": (5, 13),
    "G": (6, 15),
    "H": (7, 17),
    "I": (8, 19),
    "J": (9, 21),
    "K": (10, 2),
    "L": (11, 4),
    "M": (12, 18),
    "N": (13, 20),
    "O": (14, 11),
    "P": (15, 3),
    "Q": (16, 6),
    "R": (17, 8),
    "S": (18, 12),
    "T": (19, 14),
    "U": (20, 16),
    "V": (21, 10),
    "W": (22, 22),
    "X": (23, 25),
    "Y": (24, 24),
    "Z": (25, 23),
}
_CIN_REMAINDERS: list[str] = list(string.ascii_uppercase)

_OMOCODIA: dict[str, str] = {
    "0": "L",
    "1": "M",
    "2": "N",
    "3": "P",
    "4": "Q",
    "5": "R",
    "6": "S",
    "7": "T",
    "8": "U",
    "9": "V",
}
_OMOCODIA_DIGITS: str = "".join(list(_OMOCODIA))
_OMOCODIA_LETTERS: str = "".join([_OMOCODIA[digit] for digit in _OMOCODIA])
_OMOCODIA_ENCODE_TRANS: dict[int, int] = "".maketrans(
    _OMOCODIA_DIGITS, _OMOCODIA_LETTERS
)
_OMOCODIA_DECODE_TRANS: dict[int, int] = "".maketrans(
    _OMOCODIA_LETTERS, _OMOCODIA_DIGITS
)
_OMOCODIA_SUBS_INDEXES: list[int] = list(reversed([6, 7, 9, 10, 12, 13, 14]))
_OMOCODIA_SUBS_INDEXES_COMBINATIONS: list[list[int]] = [[]]
for combo_size in range(1, len(_OMOCODIA_SUBS_INDEXES) + 1):
    for combo in combinations(_OMOCODIA_SUBS_INDEXES, combo_size):
        _OMOCODIA_SUBS_INDEXES_COMBINATIONS.append(list(combo))


_DATA: dict[str, dict[str, list[dict[str, Any]]]] = get_indexed_data()

CODICEFISCALE_RE: Pattern[str] = re.compile(
    r"^"
    r"(?P<lastname>[a-z]{3})"
    r"(?P<firstname>[a-z]{3})"
    r"(?P<birthdate>(?P<birthdate_year>[a-z\d]{2})(?P<birthdate_month>[abcdehlmprst]{1})(?P<birthdate_day>[a-z\d]{2}))"  # noqa: B950, E501
    r"(?P<birthplace>[a-z]{1}[a-z\d]{3})"
    r"(?P<cin>[a-z]{1})$",
    re.IGNORECASE,
)


def _get_consonants(s: str) -> list[str]:
    return [char for char in s if char in _CONSONANTS]


def _get_vowels(s: str) -> list[str]:
    return [char for char in s if char in _VOWELS]


def _get_consonants_and_vowels(
    consonants: list[str],
    vowels: list[str],
) -> str:
    return "".join(list(consonants[:3] + vowels[:3] + (["X"] * 3))[:3]).upper()


def _get_date(
    date: datetime | str | None,
    separator: str = "-",
) -> datetime | None:
    if not date:
        return None
    if isinstance(date, datetime):
        date = date.replace(tzinfo=None)
        return date
    date_slug = slugify(date)
    date_parts = date_slug.split("-")[:3]
    date_parser_options = (
        {
            "yearfirst": True,
        }
        if len(date_parts[0]) == 4
        else {
            "dayfirst": True,
        }
    )
    try:
        date_obj = date_parser.parse(
            date_slug,
            parserinfo=date_parser.parserinfo(**date_parser_options),
        )
        date_obj = date_obj.replace(tzinfo=None)
        return date_obj
    except ValueError:
        return None


def _get_birthplace(
    birthplace: str,
    birthdate: datetime | str | None = None,
) -> dict[str, dict[str, Any]] | None:
    birthplace_slug = slugify(birthplace)
    birthplace_code = birthplace_slug.upper()
    birthplaces_options = _DATA["municipalities"].get(
        birthplace_slug,
        _DATA["countries"].get(
            birthplace_slug,
            _DATA["codes"].get(
                birthplace_code,
            ),
        ),
    )
    if not birthplaces_options:
        return None

    birthdate_date = _get_date(birthdate)
    if not birthdate_date:
        return birthplaces_options[0].copy()

    # search birthplace that has been created before / deleted after birthdate
    for birthplace_option in birthplaces_options:
        date_created = _get_date(birthplace_option["date_created"]) or datetime.min
        date_deleted = _get_date(birthplace_option["date_deleted"]) or datetime.max
        # print(birthdate_date, date_created, date_deleted)
        if birthdate_date >= date_created and birthdate_date <= date_deleted:
            return birthplace_option.copy()

    return _get_birthplace_fallback(birthplaces_options, birthdate_date)


def _get_birthplace_fallback(
    birthplaces_options: list[dict[str, Any]],
    birthdate_date: datetime,
) -> dict[str, dict[str, Any]] | None:
    # avoid wrong birthplace code error when birthdate falls in
    # missing date-range in the data-source even if birthplace code is valid
    birthplaces_options_count = len(birthplaces_options)
    if birthplaces_options_count > 1:
        for index in range(birthplaces_options_count - 1):
            birthplace_option = birthplaces_options[index]
            birthplace_option_next = birthplaces_options[(index + 1)]
            date_deleted = _get_date(birthplace_option["date_deleted"])
            date_created = _get_date(birthplace_option_next["date_created"])
            if date_deleted and date_created:
                if birthdate_date >= date_deleted and date_deleted <= date_created:
                    # the birthdate is in between a deleted munipality and a created one
                    # if the deleted one has a very short active time delta,
                    # it means that probably the deleted_at value is wrong
                    date_created = _get_date(birthplace_option["date_created"])
                    date_deleted = _get_date(birthplace_option["date_deleted"])
                    if date_created and date_deleted:
                        date_delta = date_deleted - date_created
                        if date_delta <= timedelta(days=1):
                            return birthplace_option.copy()
                    return birthplace_option_next.copy()

    # Fix issues #210, #213
    # sometimes the code has been assigned after date of birth and
    # the municipality was not yet active at birthdate time,
    # let's return the first municipality created after birthdate_date
    for index in range(birthplaces_options_count):
        birthplace_option = birthplaces_options[index]
        date_created = _get_date(birthplace_option["date_created"])
        if date_created:
            if birthdate_date <= date_created:
                return birthplace_option.copy()
    return None


def _get_omocode(
    code: str,
    subs: list[int],
    trans: dict[int, int],
) -> str:
    code_chars = list(code[0:15])
    for i in subs:
        code_chars[i] = code_chars[i].translate(trans)
    code = "".join(code_chars)
    code_cin = encode_cin(code)
    code += code_cin
    return code


def _get_omocodes(code: str) -> list[str]:
    code_root = _get_omocode(
        code, subs=_OMOCODIA_SUBS_INDEXES, trans=_OMOCODIA_DECODE_TRANS
    )
    codes = [
        _get_omocode(code_root, subs=subs, trans=_OMOCODIA_ENCODE_TRANS)
        for subs in _OMOCODIA_SUBS_INDEXES_COMBINATIONS
    ]
    return codes


def encode_lastname(lastname: str) -> str:
    """
    Encode lastname to the code used in italian fiscal code.

    :param lastname: The lastname
    :type lastname: string

    :returns: The code used in italian fiscal code
    :rtype: string
    """
    lastname_slug = slugify(lastname)
    lastname_consonants = _get_consonants(lastname_slug)
    lastname_vowels = _get_vowels(lastname_slug)
    lastname_code = _get_consonants_and_vowels(lastname_consonants, lastname_vowels)
    return lastname_code


def encode_firstname(firstname: str) -> str:
    """
    Encodes firstname to the code used in italian fiscal code.

    :param firstname: The firstname
    :type firstname: string

    :returns: The code used in italian fiscal code
    :rtype: string
    """
    firstname_slug = slugify(firstname)
    firstname_consonants = _get_consonants(firstname_slug)

    if len(firstname_consonants) > 3:
        del firstname_consonants[1]

    firstname_vowels = _get_vowels(firstname_slug)
    firstname_code = _get_consonants_and_vowels(firstname_consonants, firstname_vowels)
    return firstname_code


def encode_birthdate(
    birthdate: datetime | str | None,
    gender: Literal["m", "M", "f", "F"],
) -> str:
    """
    Encodes birthdate to the code used in italian fiscal code.

    :param birthdate: The birthdate
    :type birthdate: datetime or string
    :param gender: The gender, 'M' or 'F'
    :type gender: string

    :returns: The code used in italian fiscal code
    :rtype: string
    """
    if not birthdate:
        raise ValueError("[codicefiscale] 'birthdate' argument cant be None")
    date = _get_date(birthdate)
    if not date:
        raise ValueError("[codicefiscale] 'date' argument cant be None")

    if not gender:
        raise ValueError("[codicefiscale] 'gender' argument cant be None")
    gender_code = gender.upper()
    if gender_code not in ("M", "F"):
        raise ValueError("[codicefiscale] 'gender' argument must be 'M' or 'F'")

    year_code = str(date.year)[2:]
    month_code = _MONTHS[date.month - 1]
    day_code = str(date.day + (40 if gender_code == "F" else 0)).zfill(2).upper()
    date_code = f"{year_code}{month_code}{day_code}"
    return date_code


def encode_birthplace(
    birthplace: str,
    birthdate: datetime | str | None = None,
) -> str | None:
    """
    Encodes birthplace to the code used in italian fiscal code.

    :param birthplace: The birthplace
    :type birthplace: string

    :returns: The code used in italian fiscal code
    :rtype: string
    """
    if not birthplace:
        raise ValueError("[codicefiscale] 'birthplace' argument cant be None")

    birthplace_without_province = re.split(r",|\(", birthplace)[0]
    birthplace_data = _get_birthplace(
        birthplace,
        birthdate,
    ) or _get_birthplace(
        birthplace_without_province,
        birthdate,
    )

    if not birthplace_data:
        raise ValueError(
            "[codicefiscale] 'birthplace' / 'birthdate' arguments "
            f"({birthplace!r} / {birthdate!r}) not mapped to code"
        )

    birthplace_code = str(birthplace_data["code"])
    return birthplace_code


def encode_cin(code: str) -> str:
    """
    Encodes cin to the code used in italian fiscal code.

    :param code: The code
    :type code: string

    :returns: The code used in italian fiscal code
    :rtype: string
    """
    if not code:
        raise ValueError("[codicefiscale] 'code' argument cant be None")

    code_len = len(code)
    if code_len not in [15, 16]:
        raise ValueError(
            f"[codicefiscale] 'code' length must be 15 or 16, not: {code_len}"
        )

    cin_tot = 0
    for i, char in enumerate(code[0:15]):
        cin_tot += _CIN[char][int(bool((i + 1) % 2))]
    cin_code = _CIN_REMAINDERS[cin_tot % 26]

    # print(cin_code)
    return cin_code


def encode(
    lastname: str,
    firstname: str,
    gender: Literal["m", "M", "f", "F"],
    birthdate: datetime | str | None,
    birthplace: str,
) -> str:
    """
    Encodes the italian fiscal code.

    :param lastname: The lastname
    :type lastname: string
    :param firstname: The firstname
    :type firstname: string
    :param gender: The gender, 'M' or 'F'
    :type gender: string
    :param birthdate: The birthdate
    :type birthdate: datetime or string
    :param birthplace: The birthplace
    :type birthplace: string

    :returns: The italian fiscal code
    :rtype: string
    """

    lastname_code = encode_lastname(lastname)
    firstname_code = encode_firstname(firstname)
    birthdate_code = encode_birthdate(birthdate, gender)
    birthplace_code = encode_birthplace(birthplace, birthdate)
    code = f"{lastname_code}{firstname_code}{birthdate_code}{birthplace_code}"
    cin_code = encode_cin(code)
    code = f"{code}{cin_code}"

    # raise ValueError if code is not valid
    decode(code)
    return code


def decode_raw(code: str) -> dict[str, str]:
    """
    Decodes the raw data associated to the code.

    :param code: The code
    :type code: string

    :returns: The raw data associated to the code.
    :rtype: dict
    """
    code = slugify(code)
    code = code.replace("-", "")
    code = code.upper()

    match = CODICEFISCALE_RE.match(code)
    if not match:
        raise ValueError(f"[codicefiscale] invalid syntax: {code}")

    data = {
        "code": code,
        "lastname": match["lastname"],
        "firstname": match["firstname"],
        "birthdate": match["birthdate"],
        "birthdate_year": match["birthdate_year"],
        "birthdate_month": match["birthdate_month"],
        "birthdate_day": match["birthdate_day"],
        "birthplace": match["birthplace"],
        "cin": match["cin"],
    }

    return data


def decode(code: str) -> dict[str, Any]:
    """
    Decodes the italian fiscal code.

    :param code: The code
    :type code: string

    :returns: The data associated to the code and some additional info.
    :rtype: dict
    """
    raw = decode_raw(code)

    code = raw["code"]

    birthdate_year = int(raw["birthdate_year"].translate(_OMOCODIA_DECODE_TRANS))
    birthdate_month = _MONTHS.index(raw["birthdate_month"]) + 1
    birthdate_day = int(raw["birthdate_day"].translate(_OMOCODIA_DECODE_TRANS))

    if birthdate_day > 40:
        birthdate_day -= 40
        gender = "F"
    else:
        gender = "M"

    current_year = datetime.now().year
    current_year_century_prefix = str(current_year)[0:-2]
    birthdate_year_suffix = str(birthdate_year).zfill(2)
    birthdate_year = int(f"{current_year_century_prefix}{birthdate_year_suffix}")
    if birthdate_year > current_year:
        birthdate_year -= 100

    birthdate_or_birthplace_error = None
    for _ in range(2):
        birthdate_str = f"{birthdate_year}/{birthdate_month}/{birthdate_day}"
        try:
            birthdate = _get_date(birthdate_str, separator="/")
            if not birthdate:
                raise ValueError(f"[codicefiscale] invalid date: {birthdate_str}")

            birthplace_code = raw["birthplace"][0] + raw["birthplace"][1:].translate(
                _OMOCODIA_DECODE_TRANS
            )
            birthplace = _get_birthplace(birthplace_code, birthdate)
            # print(birthplace)
            if not birthplace:
                raise ValueError(
                    "[codicefiscale] wrong birthplace code: "
                    f"{birthplace_code!r} / birthdate: {birthdate.isoformat()!r}."
                )
            break
        except ValueError as error:
            # attempt to handle people over 100 years old
            if birthdate_or_birthplace_error is None:
                birthdate_or_birthplace_error = error
            birthdate_year -= 100
    else:
        # raise the first raised error
        if birthdate_or_birthplace_error:
            raise birthdate_or_birthplace_error

    cin = raw["cin"]
    cin_check = encode_cin(code)
    # print(cin, cin_check)
    if cin != cin_check:
        raise ValueError(
            "[codicefiscale] wrong CIN (Control Internal Number): "
            f"expected {cin_check!r}, found {cin!r}"
        )

    data = {
        "code": code,
        "omocodes": _get_omocodes(code),
        "gender": gender,
        "birthdate": birthdate,
        "birthplace": birthplace,
        "raw": raw,
    }

    # print(data)
    return data


def is_omocode(code: str) -> bool:
    """
    Determines whether the specified code is omocode or not.

    :param code: The code
    :type code: string

    :returns: True if the specified code is omocode, False otherwise.
    :rtype: boolean
    """
    data = decode(code)
    codes = data["omocodes"]
    codes.pop(0)
    return code in codes


def is_valid(code: str) -> bool:
    """
    Determines whether the specified code is valid.

    :param code: The code
    :type code: string

    :returns: True if the specified code is valid, False otherwise.
    :rtype: boolean
    """
    try:
        decode(code)
        return True
    except ValueError:
        return False
