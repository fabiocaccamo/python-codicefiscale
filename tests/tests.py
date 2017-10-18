# -*- coding: utf-8 -*-

from datetime import datetime

from codicefiscale import codicefiscale
from codicefiscale import version

import unittest


class CodiceFiscaleTestCase(unittest.TestCase):

    def test_encode_surname(self):

        data = [
            {
                'input':'',
                'result':'XXX',
            },
            {
                'input':'Caccamo',
                'result':'CCC',
            },
            {
                'input':'Fò',
                'result':'FOX',
            }
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            self.assertEqual(
                codicefiscale.encode_surname(obj['input']),
                obj['result'])

    def test_encode_name(self):

        data = [
            {
                'input':'',
                'result':'XXX',
            },
            {
                'input':'Alessandro',
                'result':'LSN',
            },
            {
                'input':'Dario',
                'result':'DRA',
            },
            {
                'input':'Fabio',
                'result':'FBA',
            },
            {
                'input':'Giovanni',
                'result':'GNN',
            },
            {
                'input':'Hu',
                'result':'HUX',
            },
            {
                'input':'Maria',
                'result':'MRA',
            },
            {
                'input':'Michele',
                'result':'MHL',
            }
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            self.assertEqual(
                codicefiscale.encode_name(obj['input']),
                obj['result'])

    def test_encode_birthdate_formats(self):

        data = [
            {
                'input':datetime(1985, 4, 3),
                'result':'85D03',
            },
            {
                'input':'03 04 1985',
                'result':'85D03',
            },
            {
                'input':'03/04/1985',
                'result':'85D03',
            },
            {
                'input':'03-04-1985',
                'result':'85D03',
            },
            {
                'input':'03.04.1985',
                'result':'85D03',
            },
            {
                'input':'3/4/1985',
                'result':'85D03',
            },
            {
                'input':'3-4-1985',
                'result':'85D03',
            },
            {
                'input':'3.4.1985',
                'result':'85D03',
            },
            {
                'input':'1985 04 03',
                'result':'85D03',
            },
            {
                'input':'1985/04/03',
                'result':'85D03',
            },
            {
                'input':'1985-04-03',
                'result':'85D03',
            },
            {
                'input':'1985.04.03',
                'result':'85D03',
            },
            {
                'input':'1985/4/3',
                'result':'85D03',
            },
            {
                'input':'1985-4-3',
                'result':'85D03',
            },
            {
                'input':'1985.4.3',
                'result':'85D03',
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            self.assertEqual(
                codicefiscale.encode_birthdate(obj['input'], 'M'),
                obj['result'])

    def test_encode_birthdate_invalid_arguments(self):

        with self.assertRaises(ValueError):
            codicefiscale.encode_birthdate(None, 'M')

        with self.assertRaises(ValueError):
            codicefiscale.encode_birthdate('03/04/1985', None)

        with self.assertRaises(ValueError):
            codicefiscale.encode_birthdate('03/04/1985', 'X')

        with self.assertRaises(ValueError):
            codicefiscale.encode_birthdate('1985/1985/1985', 'M')

    def test_encode_birthdate_sex(self):

        data = [
            {
                'input':['03/04/1985', 'M'],
                'result':'85D03',
            },
            {
                'input':['03/04/1985', 'F'],
                'result':'85D43',
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            self.assertEqual(
                codicefiscale.encode_birthdate(*obj['input']),
                obj['result'])

    def test_encode_birthplace_italy(self):

        data = [
            {
                'input':'Torino, Italy',
                'result':'L219',
            },
            {
                'input':'Torino (TO), Italy',
                'result':'L219',
            },
            {
                'input':'Torino (TO)',
                'result':'L219',
            },
            {
                'input':'Torino',
                'result':'L219',
            },
            {
                'input':'L219',
                'result':'L219',
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            self.assertEqual(
                codicefiscale.encode_birthplace(obj['input']),
                obj['result'])

    def test_encode_birthplace_foreign_country(self):

        data = [
            {
                'input':'Lettonia',
                'result':'Z145',
            },
            {
                'input':'Giappone',
                'result':'Z219',
            },
            {
                'input':'Marocco',
                'result':'Z330',
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            self.assertEqual(
                codicefiscale.encode_birthplace(obj['input']),
                obj['result'])

    def test_encode_birthplace_invalid_arguments(self):

        with self.assertRaises(ValueError):
            codicefiscale.encode_birthplace(None)

        with self.assertRaises(ValueError):
            codicefiscale.encode_birthplace('Area 51')

    def test_encode_cin(self):

        data = [
            {
                'input':'CCCFBA85D03L219',
                'result':'P',
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            self.assertEqual(
                codicefiscale.encode_cin(obj['input']),
                obj['result'])

    def test_encode_cin_invalid_arguments(self):

        with self.assertRaises(ValueError):
            codicefiscale.encode_cin(None)

        with self.assertRaises(ValueError):
            codicefiscale.encode_cin('CCCFBA85D03')

    def test_encode(self):

        data = [
            {
                'input': { 'surname':'Ait Hadda', 'name':'Saad', 'sex':'M', 'birthdate':'08/09/1995', 'birthplace':'Marocco' },
                'result':'THDSDA95P08Z330H',
            },
            {
                'input': { 'surname':'Belousovs', 'name':'Olegs', 'sex':'M', 'birthdate':'22/03/1984', 'birthplace':'Lettonia' },
                'result':'BLSLGS84C22Z145O',
            },
            {
                'input': { 'surname':'Bruno', 'name':'Giovanni', 'sex':'M', 'birthdate':'26/02/1971', 'birthplace':'Torino' },
                'result':'BRNGNN71B26L219T',
            },
            {
                'input': { 'surname':'Caccamo', 'name':'Fabio', 'sex':'M', 'birthdate':'03/04/1985', 'birthplace':'Torino' },
                'result':'CCCFBA85D03L219P',
            },
            {
                'input': { 'surname':'Gomba', 'name':'Alessandro', 'sex':'M', 'birthdate':'05/01/1984', 'birthplace':'Pinerolo' },
                'result':'GMBLSN84A05G674H',
            },
            {
                'input': { 'surname':'Martini', 'name':'Maria', 'sex':'F', 'birthdate':'16/12/1983', 'birthplace':'Anagni' },
                'result':'MRTMRA83T56A269B',
            },
            {
                'input': { 'surname':'Panella', 'name':'Michele', 'sex':'M', 'birthdate':'27/10/1979', 'birthplace':'San Severo (FG)' },
                'result':'PNLMHL79R27I158P',
            },
            {
                'input': { 'surname':'Quatrini', 'name':'Dario', 'sex':'M', 'birthdate':'13/09/1971', 'birthplace':'Pavia' },
                'result':'QTRDRA71P13G388J',
            },
            {
                'input': { 'surname':'Takakura', 'name':'Yuuki', 'sex':'F', 'birthdate':'28/02/1987', 'birthplace':'Torino' },
                'result':'TKKYKU87B68L219F',
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            code = codicefiscale.encode(**obj['input'])
            self.assertEqual(code, obj['result'])

        for obj in data:
            obj['input']['omocodes'] = True
            # with self.subTest(obj=obj):
            codes = codicefiscale.encode(**obj['input'])
            self.assertEqual(8, len(codes))
            self.assertEqual(codes[0], obj['result'])

    def test_decode(self):

        data = [
            {
                'input':'THDSDA95P08Z330H',
                'result': { 'sex':'M', 'birthdate':'08/09/1995', 'birthplace':'Marocco' },
            },
            {
                'input':'BLSLGS84C22Z145O',
                'result': { 'sex':'M', 'birthdate':'22/03/1984', 'birthplace':'Lettonia' },
            },
            {
                'input':'BRNGNN71B26L219T',
                'result': { 'sex':'M', 'birthdate':'26/02/1971', 'birthplace':'Torino' },
            },
            {
                'input':'CCCFBA85D03L219P',
                'result': { 'sex':'M', 'birthdate':'03/04/1985', 'birthplace':'Torino' },
            },
            {
                'input':'GMBLSN84A05G674H',
                'result': { 'sex':'M', 'birthdate':'05/01/1984', 'birthplace':'Pinerolo' },
            },
            {
                'input':'MRTMRA83T56A269B',
                'result': { 'sex':'F', 'birthdate':'16/12/1983', 'birthplace':'Anagni' },
            },
            {
                'input':'PNLMHL79R27I158P',
                'result': { 'sex':'M', 'birthdate':'27/10/1979', 'birthplace':'San Severo' },
            },
            {
                'input':'QTRDRA71P13G388J',
                'result': { 'sex':'M', 'birthdate':'13/09/1971', 'birthplace':'Pavia' },
            },
            {
                'input':'TKKYKU87B68L219F',
                'result': { 'sex':'F', 'birthdate':'28/02/1987', 'birthplace':'Torino' },
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):

            result = obj['result']
            obj_decoded = codicefiscale.decode(obj['input'])
            # print(obj_decoded)

            sex = obj_decoded.get('sex')
            self.assertFalse(sex is None)
            self.assertEqual(sex, result['sex'])

            birthdate = obj_decoded.get('birthdate')
            self.assertFalse(birthdate is None)
            self.assertEqual(birthdate,
                datetime.strptime(result['birthdate'], '%d/%m/%Y'))

            birthplace = obj_decoded.get('birthplace')
            self.assertFalse(birthplace is None)
            self.assertEqual(birthplace['name'].upper(),
                result['birthplace'].upper())

    def test_decode_invalid_syntax(self):

        # invalid surname
        with self.assertRaises(ValueError):
            codicefiscale.decode('CC0FBA85X03L219P')

        # invalid name
        with self.assertRaises(ValueError):
            codicefiscale.decode('CCCFB085X03L219P')

        # invalid date-year
        with self.assertRaises(ValueError):
            codicefiscale.decode('CCCFBA8XD03L219S')

        # invalid date-month
        with self.assertRaises(ValueError):
            codicefiscale.decode('CCCFBA85X03L219P')

        # invalid date-day
        with self.assertRaises(ValueError):
            codicefiscale.decode('CCCFBA85D00L219P')

    def test_decode_omocodia(self):
        data = [
            {
                'input':'CCCFBA85D03L219P',
                'result': { 'sex':'M', 'birthdate':'03/04/1985', 'birthplace':'Torino' },
            },
            {
                'input':'CCCFBA85D03L21VE',
                'result': { 'sex':'M', 'birthdate':'03/04/1985', 'birthplace':'Torino' },
            },
            {
                'input':'CCCFBA85D03L2MVP',
                'result': { 'sex':'M', 'birthdate':'03/04/1985', 'birthplace':'Torino' },
            },
            {
                'input':'CCCFBA85D03LNMVE',
                'result': { 'sex':'M', 'birthdate':'03/04/1985', 'birthplace':'Torino' },
            },
            {
                'input':'CCCFBA85D0PLNMVA',
                'result': { 'sex':'M', 'birthdate':'03/04/1985', 'birthplace':'Torino' },
            },
            {
                'input':'CCCFBA85DLPLNMVL',
                'result': { 'sex':'M', 'birthdate':'03/04/1985', 'birthplace':'Torino' },
            },
            {
                'input':'CCCFBA8RDLPLNMVX',
                'result': { 'sex':'M', 'birthdate':'03/04/1985', 'birthplace':'Torino' },
            },
            {
                'input':'CCCFBAURDLPLNMVU',
                'result': { 'sex':'M', 'birthdate':'03/04/1985', 'birthplace':'Torino' },
            },
        ]

        codes = [obj['input'] for obj in data]

        for obj in data:
            # with self.subTest(obj=obj):

            code = obj['input']
            result = obj['result']
            obj_decoded = codicefiscale.decode(code)

            sex = obj_decoded.get('sex')
            self.assertFalse(sex is None)
            self.assertEqual(sex, result['sex'])

            birthdate = obj_decoded.get('birthdate')
            self.assertFalse(birthdate is None)
            self.assertEqual(birthdate,
                datetime.strptime(result['birthdate'], '%d/%m/%Y'))

            birthplace = obj_decoded.get('birthplace')
            self.assertFalse(birthplace is None)
            self.assertEqual(birthplace['name'].upper(),
                result['birthplace'].upper())

            omocodes = obj_decoded.get('omocodes', [])
            self.assertEqual(8, len(omocodes))
            self.assertEqual(omocodes, codes)

    def test_is_omocode(self):

        self.assertFalse(codicefiscale.is_omocode('CCCFBA85D03L219P'))
        self.assertTrue(codicefiscale.is_omocode('CCCFBA85D03L21VE'))
        self.assertTrue(codicefiscale.is_omocode('CCCFBA85D03L2MVP'))
        self.assertTrue(codicefiscale.is_omocode('CCCFBA85D03LNMVE'))
        self.assertTrue(codicefiscale.is_omocode('CCCFBA85D0PLNMVA'))
        self.assertTrue(codicefiscale.is_omocode('CCCFBA85DLPLNMVL'))
        self.assertTrue(codicefiscale.is_omocode('CCCFBA8RDLPLNMVX'))
        self.assertTrue(codicefiscale.is_omocode('CCCFBAURDLPLNMVU'))

    def test_is_valid(self):

        self.assertTrue(codicefiscale.is_valid('CCCFBA85D03L219P'))
        self.assertTrue(codicefiscale.is_valid('CCC FBA 85 D03 L219 P'))
        self.assertTrue(codicefiscale.is_valid('CCC-FBA-85-D03-L219-P'))

        self.assertFalse(codicefiscale.is_valid('CCCFBA85D03L219PP')) # too long
        self.assertFalse(codicefiscale.is_valid('CCCFBA85D03L219B')) # wrong CIN
        self.assertFalse(codicefiscale.is_valid('CCCFBA85D03L219')) # too short
        self.assertFalse(codicefiscale.is_valid('CCCFBA85D00L219')) # wrong birthdate day
        self.assertFalse(codicefiscale.is_valid('CCCFBA85D99L219')) # wrong birthdate day


if __name__ == '__main__':
    unittest.main()
