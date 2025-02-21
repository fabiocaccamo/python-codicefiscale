import argparse
import json
import subprocess
from io import StringIO
from unittest import mock

from codicefiscale import __version__
from codicefiscale.cli import run, run_with_args


def assert_output(command, expected_output):
    output = subprocess.check_output(command, shell=True).decode("utf-8").strip()
    assert output == expected_output


def test_version():
    with mock.patch("sys.stdout", new=StringIO()) as fake_output:
        args = argparse.Namespace(
            subcommand=None,
            version=True,
        )
        run_with_args(args)
        output = fake_output.getvalue().strip()
        assert output == __version__


def test_version_from_command_line():
    assert_output("python -m codicefiscale --version", __version__)


def test_main_without_args():
    with mock.patch("sys.stdout", new=StringIO()) as fake_output:
        with mock.patch("sys.argv", ["__main__"]):
            run()
            output = fake_output.getvalue().strip()
            assert output == "For more info run: 'python -m codicefiscale --help'"


def test_main_without_args_from_command_line():
    assert_output(
        "python -m codicefiscale",
        "For more info run: 'python -m codicefiscale --help'",
    )


def test_encode():
    with mock.patch("sys.stdout", new=StringIO()) as fake_output:
        args = argparse.Namespace(
            firstname="Mario",
            lastname="Rossi",
            gender="M",
            birthdate="01/01/1990",
            birthplace="Roma,RM",
            subcommand="encode",
        )
        run_with_args(args)
        output = fake_output.getvalue().strip()
        assert output == "RSSMRA90A01H501W"


def test_encode_from_command_line():
    assert_output(
        (
            "python -m codicefiscale encode "
            "--firstname 'Mario' "
            "--lastname 'Rossi' "
            "--gender 'M' "
            "--birthdate '01/01/1990' "
            "--birthplace 'Roma' "
        ),
        "RSSMRA90A01H501W",
    )


def test_encode_with_wrong_birthplace():
    with mock.patch("sys.stderr", new=StringIO()) as fake_output:
        args = argparse.Namespace(
            firstname="Mario",
            lastname="Rossi",
            gender="M",
            birthdate="01/01/1990",
            birthplace="Romaaa,RM",
            subcommand="encode",
        )
        run_with_args(args)
        output = fake_output.getvalue().strip()
        assert output == (
            "[codicefiscale] 'birthplace' / 'birthdate' arguments "
            "('Romaaa,RM' / '01/01/1990') not mapped to code"
        )


def test_decode_without_omocodes():
    with mock.patch("sys.stdout", new=StringIO()) as fake_output:
        args = argparse.Namespace(
            code="RSSMRA90A01H501W",
            omocodes=False,
            subcommand="decode",
        )
        run_with_args(args)
        output = fake_output.getvalue().strip()
        assert (
            output
            == """
{
    "code": "RSSMRA90A01H501W",
    "gender": "M",
    "birthdate": "1990-01-01T00:00:00",
    "birthplace": {
        "active": false,
        "code": "H501",
        "date_created": "1938-07-27T00:00:00",
        "date_deleted": "1990-03-24T00:00:00",
        "name": "Roma",
        "name_alt": "",
        "name_alt_trans": "",
        "name_slugs": [
            "roma"
        ],
        "name_trans": "Roma",
        "province": "RM"
    },
    "raw": {
        "code": "RSSMRA90A01H501W",
        "lastname": "RSS",
        "firstname": "MRA",
        "birthdate": "90A01",
        "birthdate_year": "90",
        "birthdate_month": "A",
        "birthdate_day": "01",
        "birthplace": "H501",
        "cin": "W"
    }
}
""".strip()
        )

        output_data = json.loads(output)
        assert output_data == {
            "code": "RSSMRA90A01H501W",
            "gender": "M",
            "birthdate": "1990-01-01T00:00:00",
            "birthplace": {
                "active": False,
                "code": "H501",
                "date_created": "1938-07-27T00:00:00",
                "date_deleted": "1990-03-24T00:00:00",
                "name": "Roma",
                "name_alt": "",
                "name_alt_trans": "",
                "name_slugs": ["roma"],
                "name_trans": "Roma",
                "province": "RM",
            },
            "raw": {
                "code": "RSSMRA90A01H501W",
                "lastname": "RSS",
                "firstname": "MRA",
                "birthdate": "90A01",
                "birthdate_year": "90",
                "birthdate_month": "A",
                "birthdate_day": "01",
                "birthplace": "H501",
                "cin": "W",
            },
        }


def test_decode_without_omocodes_from_command_line():
    cmd = "python -m codicefiscale decode 'RSSMRA90A01H501W'"
    output = subprocess.check_output(cmd, shell=True).decode("UTF-8").strip()
    assert (
        output
        == """
{
    "code": "RSSMRA90A01H501W",
    "gender": "M",
    "birthdate": "1990-01-01T00:00:00",
    "birthplace": {
        "active": false,
        "code": "H501",
        "date_created": "1938-07-27T00:00:00",
        "date_deleted": "1990-03-24T00:00:00",
        "name": "Roma",
        "name_alt": "",
        "name_alt_trans": "",
        "name_slugs": [
            "roma"
        ],
        "name_trans": "Roma",
        "province": "RM"
    },
    "raw": {
        "code": "RSSMRA90A01H501W",
        "lastname": "RSS",
        "firstname": "MRA",
        "birthdate": "90A01",
        "birthdate_year": "90",
        "birthdate_month": "A",
        "birthdate_day": "01",
        "birthplace": "H501",
        "cin": "W"
    }
}
""".strip()
    )

    output_data = json.loads(output)
    assert output_data == {
        "code": "RSSMRA90A01H501W",
        "gender": "M",
        "birthdate": "1990-01-01T00:00:00",
        "birthplace": {
            "active": False,
            "code": "H501",
            "date_created": "1938-07-27T00:00:00",
            "date_deleted": "1990-03-24T00:00:00",
            "name": "Roma",
            "name_alt": "",
            "name_alt_trans": "",
            "name_slugs": ["roma"],
            "name_trans": "Roma",
            "province": "RM",
        },
        "raw": {
            "code": "RSSMRA90A01H501W",
            "lastname": "RSS",
            "firstname": "MRA",
            "birthdate": "90A01",
            "birthdate_year": "90",
            "birthdate_month": "A",
            "birthdate_day": "01",
            "birthplace": "H501",
            "cin": "W",
        },
    }


def test_decode_with_omocodes():
    with mock.patch("sys.stdout", new=StringIO()) as fake_output:
        args = argparse.Namespace(
            code="RSSMRA90A01H501W",
            omocodes=True,
            subcommand="decode",
        )
        run_with_args(args)
        output = fake_output.getvalue().strip()
        assert (
            output
            == """
{
    "code": "RSSMRA90A01H501W",
    "omocodes": [
        "RSSMRA90A01H501W",
        "RSSMRA90A01H50MO",
        "RSSMRA90A01H5L1H",
        "RSSMRA90A01HR01R",
        "RSSMRA90A0MH501O",
        "RSSMRA90AL1H501H",
        "RSSMRA9LA01H501H",
        "RSSMRAV0A01H501L",
        "RSSMRA90A01H5LMZ",
        "RSSMRA90A01HR0MJ",
        "RSSMRA90A0MH50MG",
        "RSSMRA90AL1H50MZ",
        "RSSMRA9LA01H50MZ",
        "RSSMRAV0A01H50MD",
        "RSSMRA90A01HRL1C",
        "RSSMRA90A0MH5L1Z",
        "RSSMRA90AL1H5L1S",
        "RSSMRA9LA01H5L1S",
        "RSSMRAV0A01H5L1W",
        "RSSMRA90A0MHR01J",
        "RSSMRA90AL1HR01C",
        "RSSMRA9LA01HR01C",
        "RSSMRAV0A01HR01G",
        "RSSMRA90ALMH501Z",
        "RSSMRA9LA0MH501Z",
        "RSSMRAV0A0MH501D",
        "RSSMRA9LAL1H501S",
        "RSSMRAV0AL1H501W",
        "RSSMRAVLA01H501W",
        "RSSMRA90A01HRLMU",
        "RSSMRA90A0MH5LMR",
        "RSSMRA90AL1H5LMK",
        "RSSMRA9LA01H5LMK",
        "RSSMRAV0A01H5LMO",
        "RSSMRA90A0MHR0MB",
        "RSSMRA90AL1HR0MU",
        "RSSMRA9LA01HR0MU",
        "RSSMRAV0A01HR0MY",
        "RSSMRA90ALMH50MR",
        "RSSMRA9LA0MH50MR",
        "RSSMRAV0A0MH50MV",
        "RSSMRA9LAL1H50MK",
        "RSSMRAV0AL1H50MO",
        "RSSMRAVLA01H50MO",
        "RSSMRA90A0MHRL1U",
        "RSSMRA90AL1HRL1N",
        "RSSMRA9LA01HRL1N",
        "RSSMRAV0A01HRL1R",
        "RSSMRA90ALMH5L1K",
        "RSSMRA9LA0MH5L1K",
        "RSSMRAV0A0MH5L1O",
        "RSSMRA9LAL1H5L1D",
        "RSSMRAV0AL1H5L1H",
        "RSSMRAVLA01H5L1H",
        "RSSMRA90ALMHR01U",
        "RSSMRA9LA0MHR01U",
        "RSSMRAV0A0MHR01Y",
        "RSSMRA9LAL1HR01N",
        "RSSMRAV0AL1HR01R",
        "RSSMRAVLA01HR01R",
        "RSSMRA9LALMH501K",
        "RSSMRAV0ALMH501O",
        "RSSMRAVLA0MH501O",
        "RSSMRAVLAL1H501H",
        "RSSMRA90A0MHRLMM",
        "RSSMRA90AL1HRLMF",
        "RSSMRA9LA01HRLMF",
        "RSSMRAV0A01HRLMJ",
        "RSSMRA90ALMH5LMC",
        "RSSMRA9LA0MH5LMC",
        "RSSMRAV0A0MH5LMG",
        "RSSMRA9LAL1H5LMV",
        "RSSMRAV0AL1H5LMZ",
        "RSSMRAVLA01H5LMZ",
        "RSSMRA90ALMHR0MM",
        "RSSMRA9LA0MHR0MM",
        "RSSMRAV0A0MHR0MQ",
        "RSSMRA9LAL1HR0MF",
        "RSSMRAV0AL1HR0MJ",
        "RSSMRAVLA01HR0MJ",
        "RSSMRA9LALMH50MC",
        "RSSMRAV0ALMH50MG",
        "RSSMRAVLA0MH50MG",
        "RSSMRAVLAL1H50MZ",
        "RSSMRA90ALMHRL1F",
        "RSSMRA9LA0MHRL1F",
        "RSSMRAV0A0MHRL1J",
        "RSSMRA9LAL1HRL1Y",
        "RSSMRAV0AL1HRL1C",
        "RSSMRAVLA01HRL1C",
        "RSSMRA9LALMH5L1V",
        "RSSMRAV0ALMH5L1Z",
        "RSSMRAVLA0MH5L1Z",
        "RSSMRAVLAL1H5L1S",
        "RSSMRA9LALMHR01F",
        "RSSMRAV0ALMHR01J",
        "RSSMRAVLA0MHR01J",
        "RSSMRAVLAL1HR01C",
        "RSSMRAVLALMH501Z",
        "RSSMRA90ALMHRLMX",
        "RSSMRA9LA0MHRLMX",
        "RSSMRAV0A0MHRLMB",
        "RSSMRA9LAL1HRLMQ",
        "RSSMRAV0AL1HRLMU",
        "RSSMRAVLA01HRLMU",
        "RSSMRA9LALMH5LMN",
        "RSSMRAV0ALMH5LMR",
        "RSSMRAVLA0MH5LMR",
        "RSSMRAVLAL1H5LMK",
        "RSSMRA9LALMHR0MX",
        "RSSMRAV0ALMHR0MB",
        "RSSMRAVLA0MHR0MB",
        "RSSMRAVLAL1HR0MU",
        "RSSMRAVLALMH50MR",
        "RSSMRA9LALMHRL1Q",
        "RSSMRAV0ALMHRL1U",
        "RSSMRAVLA0MHRL1U",
        "RSSMRAVLAL1HRL1N",
        "RSSMRAVLALMH5L1K",
        "RSSMRAVLALMHR01U",
        "RSSMRA9LALMHRLMI",
        "RSSMRAV0ALMHRLMM",
        "RSSMRAVLA0MHRLMM",
        "RSSMRAVLAL1HRLMF",
        "RSSMRAVLALMH5LMC",
        "RSSMRAVLALMHR0MM",
        "RSSMRAVLALMHRL1F",
        "RSSMRAVLALMHRLMX"
    ],
    "gender": "M",
    "birthdate": "1990-01-01T00:00:00",
    "birthplace": {
        "active": false,
        "code": "H501",
        "date_created": "1938-07-27T00:00:00",
        "date_deleted": "1990-03-24T00:00:00",
        "name": "Roma",
        "name_alt": "",
        "name_alt_trans": "",
        "name_slugs": [
            "roma"
        ],
        "name_trans": "Roma",
        "province": "RM"
    },
    "raw": {
        "code": "RSSMRA90A01H501W",
        "lastname": "RSS",
        "firstname": "MRA",
        "birthdate": "90A01",
        "birthdate_year": "90",
        "birthdate_month": "A",
        "birthdate_day": "01",
        "birthplace": "H501",
        "cin": "W"
    }
}
""".strip()
        )
        output_data = json.loads(output)
        assert output_data == {
            "code": "RSSMRA90A01H501W",
            "omocodes": [
                "RSSMRA90A01H501W",
                "RSSMRA90A01H50MO",
                "RSSMRA90A01H5L1H",
                "RSSMRA90A01HR01R",
                "RSSMRA90A0MH501O",
                "RSSMRA90AL1H501H",
                "RSSMRA9LA01H501H",
                "RSSMRAV0A01H501L",
                "RSSMRA90A01H5LMZ",
                "RSSMRA90A01HR0MJ",
                "RSSMRA90A0MH50MG",
                "RSSMRA90AL1H50MZ",
                "RSSMRA9LA01H50MZ",
                "RSSMRAV0A01H50MD",
                "RSSMRA90A01HRL1C",
                "RSSMRA90A0MH5L1Z",
                "RSSMRA90AL1H5L1S",
                "RSSMRA9LA01H5L1S",
                "RSSMRAV0A01H5L1W",
                "RSSMRA90A0MHR01J",
                "RSSMRA90AL1HR01C",
                "RSSMRA9LA01HR01C",
                "RSSMRAV0A01HR01G",
                "RSSMRA90ALMH501Z",
                "RSSMRA9LA0MH501Z",
                "RSSMRAV0A0MH501D",
                "RSSMRA9LAL1H501S",
                "RSSMRAV0AL1H501W",
                "RSSMRAVLA01H501W",
                "RSSMRA90A01HRLMU",
                "RSSMRA90A0MH5LMR",
                "RSSMRA90AL1H5LMK",
                "RSSMRA9LA01H5LMK",
                "RSSMRAV0A01H5LMO",
                "RSSMRA90A0MHR0MB",
                "RSSMRA90AL1HR0MU",
                "RSSMRA9LA01HR0MU",
                "RSSMRAV0A01HR0MY",
                "RSSMRA90ALMH50MR",
                "RSSMRA9LA0MH50MR",
                "RSSMRAV0A0MH50MV",
                "RSSMRA9LAL1H50MK",
                "RSSMRAV0AL1H50MO",
                "RSSMRAVLA01H50MO",
                "RSSMRA90A0MHRL1U",
                "RSSMRA90AL1HRL1N",
                "RSSMRA9LA01HRL1N",
                "RSSMRAV0A01HRL1R",
                "RSSMRA90ALMH5L1K",
                "RSSMRA9LA0MH5L1K",
                "RSSMRAV0A0MH5L1O",
                "RSSMRA9LAL1H5L1D",
                "RSSMRAV0AL1H5L1H",
                "RSSMRAVLA01H5L1H",
                "RSSMRA90ALMHR01U",
                "RSSMRA9LA0MHR01U",
                "RSSMRAV0A0MHR01Y",
                "RSSMRA9LAL1HR01N",
                "RSSMRAV0AL1HR01R",
                "RSSMRAVLA01HR01R",
                "RSSMRA9LALMH501K",
                "RSSMRAV0ALMH501O",
                "RSSMRAVLA0MH501O",
                "RSSMRAVLAL1H501H",
                "RSSMRA90A0MHRLMM",
                "RSSMRA90AL1HRLMF",
                "RSSMRA9LA01HRLMF",
                "RSSMRAV0A01HRLMJ",
                "RSSMRA90ALMH5LMC",
                "RSSMRA9LA0MH5LMC",
                "RSSMRAV0A0MH5LMG",
                "RSSMRA9LAL1H5LMV",
                "RSSMRAV0AL1H5LMZ",
                "RSSMRAVLA01H5LMZ",
                "RSSMRA90ALMHR0MM",
                "RSSMRA9LA0MHR0MM",
                "RSSMRAV0A0MHR0MQ",
                "RSSMRA9LAL1HR0MF",
                "RSSMRAV0AL1HR0MJ",
                "RSSMRAVLA01HR0MJ",
                "RSSMRA9LALMH50MC",
                "RSSMRAV0ALMH50MG",
                "RSSMRAVLA0MH50MG",
                "RSSMRAVLAL1H50MZ",
                "RSSMRA90ALMHRL1F",
                "RSSMRA9LA0MHRL1F",
                "RSSMRAV0A0MHRL1J",
                "RSSMRA9LAL1HRL1Y",
                "RSSMRAV0AL1HRL1C",
                "RSSMRAVLA01HRL1C",
                "RSSMRA9LALMH5L1V",
                "RSSMRAV0ALMH5L1Z",
                "RSSMRAVLA0MH5L1Z",
                "RSSMRAVLAL1H5L1S",
                "RSSMRA9LALMHR01F",
                "RSSMRAV0ALMHR01J",
                "RSSMRAVLA0MHR01J",
                "RSSMRAVLAL1HR01C",
                "RSSMRAVLALMH501Z",
                "RSSMRA90ALMHRLMX",
                "RSSMRA9LA0MHRLMX",
                "RSSMRAV0A0MHRLMB",
                "RSSMRA9LAL1HRLMQ",
                "RSSMRAV0AL1HRLMU",
                "RSSMRAVLA01HRLMU",
                "RSSMRA9LALMH5LMN",
                "RSSMRAV0ALMH5LMR",
                "RSSMRAVLA0MH5LMR",
                "RSSMRAVLAL1H5LMK",
                "RSSMRA9LALMHR0MX",
                "RSSMRAV0ALMHR0MB",
                "RSSMRAVLA0MHR0MB",
                "RSSMRAVLAL1HR0MU",
                "RSSMRAVLALMH50MR",
                "RSSMRA9LALMHRL1Q",
                "RSSMRAV0ALMHRL1U",
                "RSSMRAVLA0MHRL1U",
                "RSSMRAVLAL1HRL1N",
                "RSSMRAVLALMH5L1K",
                "RSSMRAVLALMHR01U",
                "RSSMRA9LALMHRLMI",
                "RSSMRAV0ALMHRLMM",
                "RSSMRAVLA0MHRLMM",
                "RSSMRAVLAL1HRLMF",
                "RSSMRAVLALMH5LMC",
                "RSSMRAVLALMHR0MM",
                "RSSMRAVLALMHRL1F",
                "RSSMRAVLALMHRLMX",
            ],
            "gender": "M",
            "birthdate": "1990-01-01T00:00:00",
            "birthplace": {
                "active": False,
                "code": "H501",
                "date_created": "1938-07-27T00:00:00",
                "date_deleted": "1990-03-24T00:00:00",
                "name": "Roma",
                "name_alt": "",
                "name_alt_trans": "",
                "name_slugs": ["roma"],
                "name_trans": "Roma",
                "province": "RM",
            },
            "raw": {
                "code": "RSSMRA90A01H501W",
                "lastname": "RSS",
                "firstname": "MRA",
                "birthdate": "90A01",
                "birthdate_year": "90",
                "birthdate_month": "A",
                "birthdate_day": "01",
                "birthplace": "H501",
                "cin": "W",
            },
        }


def test_decode_with_wrong_code():
    with mock.patch("sys.stderr", new=StringIO()) as fake_output:
        args = argparse.Namespace(
            code="RSSMRA90A01H501X",
            omocodes=False,
            subcommand="decode",
        )
        run_with_args(args)
        output = fake_output.getvalue().strip()
        assert output == (
            "[codicefiscale] wrong CIN (Control Internal Number): "
            "expected 'W', found 'X'"
        )


def test_validate():
    with mock.patch("sys.stdout", new=StringIO()) as fake_output:
        args = argparse.Namespace(
            code="RSSMRA90A01H501W",
            subcommand="validate",
        )
        run_with_args(args)
        output = fake_output.getvalue().strip()
        assert output == "✅"


def test_validate_from_command_line():
    cmd = "python -m codicefiscale validate 'RSSMRA90A01H501W'"
    output = subprocess.check_output(cmd, shell=True).decode("UTF-8").strip()
    assert output == "✅"


def test_validate_with_wrong_code():
    with mock.patch("sys.stdout", new=StringIO()) as fake_output:
        args = argparse.Namespace(
            code="RSSMRA90A01H501X",
            subcommand="validate",
        )
        run_with_args(args)
        output = fake_output.getvalue().strip()
        assert output == "❌"


def test_validate_with_wrong_code_from_command_line():
    cmd = "python -m codicefiscale validate 'RSSMRA90A01H501X'"
    output = subprocess.check_output(cmd, shell=True).decode("UTF-8").strip()
    assert output == "❌"
