# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil import parser as date_parser
from slugify import slugify

import re
import string

try:
    maketrans = ''.maketrans
except AttributeError:
    # fallback for Python 2
    maketrans = string.maketrans

from . import data


__CONSONANTS = list('bcdfghjklmnpqrstvwxyz')
__VOWELS = list('aeiou')
__MONTHS = list('ABCDEHLMPRST')
__CIN_ODDS = {
    '0': 1, '1': 0, '2': 5, '3': 7, '4': 9,
    '5': 13, '6': 15, '7': 17, '8': 19, '9': 21,
    'A': 1, 'B': 0, 'C': 5, 'D': 7, 'E': 9,
    'F': 13, 'G': 15, 'H': 17, 'I': 19, 'J': 21,
    'K': 2, 'L': 4, 'M': 18, 'N': 20, 'O': 11,
    'P': 3, 'Q': 6, 'R': 8, 'S': 12, 'T': 14,
    'U': 16, 'V': 10, 'W': 22, 'X': 25, 'Y': 24,
    'Z': 23,
}
__CIN_EVENS = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4,
    'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
    'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14,
    'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
    'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24,
    'Z': 25,
}
__CIN_REMAINDERS = list(string.ascii_uppercase)

__OMOCODIA = {
    '0': 'L', '1': 'M', '2': 'N', '3': 'P', '4': 'Q',
    '5': 'R', '6': 'S', '7': 'T', '8': 'U', '9': 'V',
}
__OMOCODIA_DIGITS = []
__OMOCODIA_LETTERS = []

for digit in __OMOCODIA:
    __OMOCODIA_DIGITS.append(digit)
    __OMOCODIA_LETTERS.append(__OMOCODIA[digit])

# omocodia translation map
__OMOCODIA_TRANS = maketrans(
    ''.join(__OMOCODIA_LETTERS), ''.join(__OMOCODIA_DIGITS))

__DATA = data.get_indexed_data(slugify)

CODICEFISCALE_RE = re.compile(r'^'
                              '([a-z]{3})'
                              '([a-z]{3})'
                              '(([a-z\d]{2})([abcdehlmprst]{1})([a-z\d]{2}))'
                              '([a-z]{1}[a-z\d]{3})'
                              '([a-z]{1})$', re.IGNORECASE)


def __get_consonants(s):
    return [char for char in s if char in __CONSONANTS]


def __get_vowels(s):
    return [char for char in s if char in __VOWELS]


def __get_consonants_and_vowels_code(consonants, vowels):
    return ''.join(list(
        consonants[:3] + vowels[:3] + (['X'] * 3)
        )[:3]).upper()


def encode_surname(surname):

    surname_slug = slugify(surname)
    surname_consonants = __get_consonants(surname_slug)
    surname_vowels = __get_vowels(surname_slug)
    surname_code = __get_consonants_and_vowels_code(
        surname_consonants, surname_vowels)
    return surname_code


def encode_name(name):

    name_slug = slugify(name)
    name_consonants = __get_consonants(name_slug)

    if len(name_consonants) > 3:
        del name_consonants[1]

    name_vowels = __get_vowels(name_slug)
    name_code = __get_consonants_and_vowels_code(
        name_consonants, name_vowels)
    return name_code


def encode_birthdate(birthdate, sex):

    if not birthdate:
        raise ValueError('[codicefiscale] '
                         '"birthdate" argument cant be None')

    if not sex:
        raise ValueError('[codicefiscale] '
                         '"sex" argument cant be None')

    sex = sex.upper()

    if sex not in ['M', 'F']:
        raise ValueError('[codicefiscale] '
                         '"sex" argument must be "M" or "F"')

    if isinstance(birthdate, datetime):
        date_obj = birthdate
    else:
        date_slug = slugify(birthdate)
        date_parts = date_slug.split('-')[:3]
        date_kwargs = {'yearfirst': True} if len(
            date_parts[0]) == 4 else {'dayfirst': True}
        try:
            date_obj = date_parser.parse(
                date_slug, **date_kwargs)
        except ValueError as e:
            raise ValueError('[codicefiscale] %s' % (str(e), ))

    year_code = str(date_obj.year)[2:]
    month_code = __MONTHS[date_obj.month - 1]
    day_code = str(date_obj.day + (40 if sex == 'F' else 0)).zfill(2).upper()

    return year_code + month_code + day_code


def encode_birthplace(birthplace):

    if not birthplace:
        raise ValueError('[codicefiscale] '
                         '"birthplace" argument cant be None')

    def find_birthplace_code(birthplace):
        birthplace_slug = slugify(birthplace)
        birthplace_code = \
            birthplace_slug[0].upper() + \
            birthplace_slug[1:].translate(__OMOCODIA_TRANS)
        birthplace_data = __DATA['municipalities'].get(
            birthplace_slug, __DATA['countries'].get(
                birthplace_slug, __DATA['codes'].get(
                    birthplace_code, {})))

        return birthplace_data.get('code', '')

    birthplace_code = \
        find_birthplace_code(birthplace) or \
        find_birthplace_code(re.split(r',|\(', birthplace)[0])

    return birthplace_code


def encode_cin(code):

    if not code:
        raise ValueError('[codicefiscale] '
                         '"code" argument cant be None')

    if len(code) not in [15, 16]:
        raise ValueError('[codicefiscale] '
                         '"code" length must be 15 or 16, not: %s' % len(code))

    cin_tot = 0
    for i, char in enumerate(code[0:15]):
        cin_tot += __CIN_ODDS[char] if (i + 1) % 2 else __CIN_EVENS[char]
    cin_code = __CIN_REMAINDERS[cin_tot % 26]

    # print(cin_code)
    return cin_code


def encode(surname, name, sex, birthdate, birthplace):

    code = ''
    code += encode_surname(surname)
    code += encode_name(name)
    code += encode_birthdate(birthdate, sex)
    code += encode_birthplace(birthplace)
    code += encode_cin(code)

    # raise ValueError if code is not valid
    decode(code)

    return code


def decode(code):

    code = slugify(code).replace('-', '').upper()

    m = CODICEFISCALE_RE.match(code)
    if not m:
        raise ValueError('[codicefiscale] '
                         'invalid syntax: %s' % (code, ))

    g = m.groups()
    # print(g)

    surname_code = g[0]
    name_code = g[1]
    birthdate_code = g[2]
    birthdate_year = g[3].translate(__OMOCODIA_TRANS)
    birthdate_month = __MONTHS.index(g[4]) + 1
    birthdate_day = int(g[5].translate(__OMOCODIA_TRANS))

    if birthdate_day > 40:
        birthdate_day -= 40
        sex = 'F'
    else:
        sex = 'M'

    birthdate_str = '%s/%s/%s' % (birthdate_year,
                                  birthdate_month,
                                  birthdate_day, )

    try:
        birthdate = datetime.strptime(birthdate_str, '%y/%m/%d')
    except ValueError:
        raise ValueError('[codicefiscale] '
                         'invalid date: %s' % (birthdate_str, ))

    birthplace_code = g[6]
    birthplace = __DATA['codes'].get(
        birthplace_code[0] +
        birthplace_code[1:].translate(__OMOCODIA_TRANS))

    cin = g[7]
    cin_check = encode_cin(code)
    # print(cin, cin_check)
    if cin != cin_check:
        raise ValueError('[codicefiscale] '
                         'wrong CIN (Control Internal Number): '
                         'expected "%s", found "%s"' % (cin_check, cin))

    data = {
        'code': code,
        # 'surname_code': surname_code,
        # 'name_code': name_code,
        'sex': sex,
        # 'birthdate_code': birthdate_code,
        'birthdate': birthdate,
        # 'birthplace_code': birthplace_code,
        'birthplace': birthplace,
        'cin': cin,
    }

    # print(data)
    return data


def is_valid(code):
    try:
        decode(code)
        return True
    except ValueError:
        return False
