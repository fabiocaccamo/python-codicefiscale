# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil import parser as date_parser
from itertools import combinations
from slugify import slugify

import fsutil
import re
import string


_CONSONANTS = list("bcdfghjklmnpqrstvwxyz")
_VOWELS = list("aeiou")
_MONTHS = list("ABCDEHLMPRST")
_CIN = {
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
_CIN_REMAINDERS = list(string.ascii_uppercase)

_OMOCODIA = {
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
_OMOCODIA_DIGITS = "".join([digit for digit in _OMOCODIA])
_OMOCODIA_LETTERS = "".join([_OMOCODIA[digit] for digit in _OMOCODIA])
_OMOCODIA_ENCODE_TRANS = "".maketrans(_OMOCODIA_DIGITS, _OMOCODIA_LETTERS)
_OMOCODIA_DECODE_TRANS = "".maketrans(_OMOCODIA_LETTERS, _OMOCODIA_DIGITS)
_OMOCODIA_SUBS_INDEXES = list(reversed([6, 7, 9, 10, 12, 13, 14]))
_OMOCODIA_SUBS_INDEXES_COMBINATIONS = [[]]
for combo_size in range(1, len(_OMOCODIA_SUBS_INDEXES) + 1):
    for combo in combinations(_OMOCODIA_SUBS_INDEXES, combo_size):
        _OMOCODIA_SUBS_INDEXES_COMBINATIONS.append(list(combo))


def _get_data(filename):
    return fsutil.read_file_json(fsutil.join_path(__file__, f"data/{filename}"))


def _get_indexed_data():
    municipalities = _get_data("municipalities.json")
    countries = _get_data("countries.json")
    data = {
        "municipalities": {},
        "countries": {},
        "codes": {},
    }

    for municipality in municipalities:
        code = municipality["code"]
        province = municipality["province"].lower()
        names = municipality["name_slugs"]
        for name in names:
            data["municipalities"][name] = municipality
            data["municipalities"][name + "-" + province] = municipality
        data["codes"].setdefault(code, [])
        data["codes"][code].append(municipality)

    for country in countries:
        code = country["code"]
        names = country["name_slugs"]
        for name in names:
            data["countries"][name] = country
        data["codes"].setdefault(code, [])
        data["codes"][code].append(country)

    return data


_DATA = _get_indexed_data()

CODICEFISCALE_RE = re.compile(
    r"^"
    r"([a-z]{3})"
    r"([a-z]{3})"
    r"(([a-z\d]{2})([abcdehlmprst]{1})([a-z\d]{2}))"
    r"([a-z]{1}[a-z\d]{3})"
    r"([a-z]{1})$",
    re.IGNORECASE,
)


def _get_consonants(s):
    return [char for char in s if char in _CONSONANTS]


def _get_vowels(s):
    return [char for char in s if char in _VOWELS]


def _get_consonants_and_vowels(consonants, vowels):
    return "".join(list(consonants[:3] + vowels[:3] + (["X"] * 3))[:3]).upper()


def _get_omocode(code, subs, trans):
    code_chars = list(code[0:15])
    for i in subs:
        code_chars[i] = code_chars[i].translate(trans)
    code = "".join(code_chars)
    code_cin = encode_cin(code)
    code += code_cin
    return code


def _get_omocodes(code):
    code_root = _get_omocode(
        code, subs=_OMOCODIA_SUBS_INDEXES, trans=_OMOCODIA_DECODE_TRANS
    )
    codes = [
        _get_omocode(code_root, subs=subs, trans=_OMOCODIA_ENCODE_TRANS)
        for subs in _OMOCODIA_SUBS_INDEXES_COMBINATIONS
    ]
    return codes


def _get_date(s):
    try:
        value = datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        value = None
    return value


def encode_surname(surname):
    """
    Encode surname to the code used in italian fiscal code.

    :param surname: The surname
    :type surname: string

    :returns: The code used in italian fiscal code
    :rtype: string
    """
    surname_slug = slugify(surname)
    surname_consonants = _get_consonants(surname_slug)
    surname_vowels = _get_vowels(surname_slug)
    surname_code = _get_consonants_and_vowels(surname_consonants, surname_vowels)
    return surname_code


def encode_name(name):
    """
    Encodes name to the code used in italian fiscal code.

    :param name: The name
    :type name: string

    :returns: The code used in italian fiscal code
    :rtype: string
    """
    name_slug = slugify(name)
    name_consonants = _get_consonants(name_slug)

    if len(name_consonants) > 3:
        del name_consonants[1]

    name_vowels = _get_vowels(name_slug)
    name_code = _get_consonants_and_vowels(name_consonants, name_vowels)
    return name_code


def encode_birthdate(birthdate, sex):
    """
    Encodes birthdate to the code used in italian fiscal code.

    :param birthdate: The birthdate
    :type birthdate: datetime or string
    :param sex: The sex, 'M' or 'F'
    :type sex: string

    :returns: The code used in italian fiscal code
    :rtype: string
    """
    if not birthdate:
        raise ValueError("[codicefiscale] 'birthdate' argument cant be None")

    if not sex:
        raise ValueError("[codicefiscale] 'sex' argument cant be None")

    sex = sex.upper()

    if sex not in ["M", "F"]:
        raise ValueError("[codicefiscale] 'sex' argument must be 'M' or 'F'")

    if isinstance(birthdate, datetime):
        date_obj = birthdate
    else:
        date_slug = slugify(birthdate)
        date_parts = date_slug.split("-")[:3]
        date_kwargs = (
            {"yearfirst": True} if len(date_parts[0]) == 4 else {"dayfirst": True}
        )
        try:
            date_obj = date_parser.parse(date_slug, **date_kwargs)
        except ValueError as e:
            raise ValueError(f"[codicefiscale] {e}")

    year_code = str(date_obj.year)[2:]
    month_code = _MONTHS[date_obj.month - 1]
    day_code = str(date_obj.day + (40 if sex == "F" else 0)).zfill(2).upper()
    date_code = year_code + month_code + day_code
    return date_code


def encode_birthplace(birthplace):
    """
    Encodes birthplace to the code used in italian fiscal code.

    :param birthplace: The birthplace
    :type birthplace: string

    :returns: The code used in italian fiscal code
    :rtype: string
    """
    if not birthplace:
        raise ValueError("[codicefiscale] 'birthplace' argument cant be None")

    def find_birthplace_code(birthplace):
        birthplace_slug = slugify(birthplace)
        birthplace_code = birthplace_slug.upper()
        birthplace_data = _DATA["municipalities"].get(
            birthplace_slug,
            _DATA["countries"].get(birthplace_slug),
        )
        if birthplace_data:
            return birthplace_data.get("code", "")
        elif birthplace_code in _DATA["codes"]:
            return birthplace_code
        else:
            return ""

    birthplace_code = find_birthplace_code(birthplace) or find_birthplace_code(
        re.split(r",|\(", birthplace)[0]
    )

    if birthplace_code == "":
        raise ValueError(
            f"[codicefiscale] 'birthplace' argument not mapped to code: ('{birthplace}' -> '')"
        )

    return birthplace_code


def encode_cin(code):
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


def encode(surname, name, sex, birthdate, birthplace):
    """
    Encodes the italian fiscal code.

    :param surname: The surname
    :type surname: string
    :param name: The name
    :type name: string
    :param sex: The sex, 'M' or 'F'
    :type sex: string
    :param birthdate: The birthdate
    :type birthdate: datetime or string
    :param birthplace: The birthplace
    :type birthplace: string

    :returns: The italian fiscal code
    :rtype: string
    """
    code = ""
    code += encode_surname(surname)
    code += encode_name(name)
    code += encode_birthdate(birthdate, sex)
    code += encode_birthplace(birthplace)
    code += encode_cin(code)

    # raise ValueError if code is not valid
    data = decode(code)
    return data["code"]


def decode_raw(code):
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

    m = CODICEFISCALE_RE.match(code)
    if not m:
        raise ValueError(f"[codicefiscale] invalid syntax: {code}")

    g = m.groups()
    # print(g)

    data = {
        "code": code,
        "surname": g[0],
        "name": g[1],
        "birthdate": g[2],
        "birthdate_year": g[3],
        "birthdate_month": g[4],
        "birthdate_day": g[5],
        "birthplace": g[6],
        "cin": g[7],
    }

    return data


def decode(code):
    """
    Decodes the italian fiscal code.

    :param code: The code
    :type code: string

    :returns: The data associated to the code and some additional info.
    :rtype: dict
    """
    raw = decode_raw(code)

    code = raw["code"]

    birthdate_year = raw["birthdate_year"].translate(_OMOCODIA_DECODE_TRANS)
    birthdate_month = _MONTHS.index(raw["birthdate_month"]) + 1
    birthdate_day = int(raw["birthdate_day"].translate(_OMOCODIA_DECODE_TRANS))

    if birthdate_day > 40:
        birthdate_day -= 40
        sex = "F"
    else:
        sex = "M"

    current_year = datetime.now().year
    current_year_century_prefix = str(current_year)[0:-2]
    birthdate_year_int = int(f"{current_year_century_prefix}{birthdate_year}")
    if birthdate_year_int > current_year:
        birthdate_year_int -= 100
    birthdate_year = str(birthdate_year_int)
    birthdate_str = f"{birthdate_year}/{birthdate_month}/{birthdate_day}"
    try:
        birthdate = datetime.strptime(birthdate_str, "%Y/%m/%d")
    except ValueError:
        raise ValueError(f"[codicefiscale] invalid date: {birthdate_str}")

    birthplace_code = raw["birthplace"][0] + raw["birthplace"][1:].translate(
        _OMOCODIA_DECODE_TRANS
    )
    birthplace = None
    birthplaces_options = _DATA["codes"].get(birthplace_code)
    for birthplace_option in birthplaces_options:
        date_created = _get_date(birthplace_option["date_created"]) or datetime.min
        date_deleted = _get_date(birthplace_option["date_deleted"]) or datetime.max
        if birthdate >= date_created and birthdate <= date_deleted:
            birthplace = birthplace_option.copy()
            break

    cin = raw["cin"]
    cin_check = encode_cin(code)
    # print(cin, cin_check)
    if cin != cin_check:
        raise ValueError(
            f"[codicefiscale] wrong CIN (Control Internal Number): expected '{cin_check}', found '{cin}'"
        )

    data = {
        "code": code,
        "omocodes": _get_omocodes(code),
        "sex": sex,
        "birthdate": birthdate,
        "birthplace": birthplace,
        "raw": raw,
    }

    # print(data)
    return data


def is_omocode(code):
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


def is_valid(code):
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
