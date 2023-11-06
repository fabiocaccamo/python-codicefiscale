import argparse
import json
import sys
from datetime import datetime
from typing import Any

from codicefiscale import __description__, __version__, codicefiscale


def _encode_from_args(args: argparse.Namespace) -> None:
    try:
        cf = codicefiscale.encode(
            lastname=args.lastname,
            firstname=args.firstname,
            gender=args.gender,
            birthdate=args.birthdate,
            birthplace=args.birthplace,
        )
    except Exception as error:
        sys.stderr.write(f"{error}\n")
    else:
        sys.stdout.write(f"{cf}\n")


def _decode_from_args(args: argparse.Namespace) -> None:
    try:
        cf_data = codicefiscale.decode(args.code)
    except Exception as error:
        sys.stderr.write(f"{error}\n")
    else:
        if not args.omocodes:
            cf_data.pop("omocodes", None)

        def default_encoder(obj: Any) -> Any:
            if isinstance(obj, datetime):
                return obj.isoformat()

        cf_output = json.dumps(
            cf_data,
            default=default_encoder,
            indent=4,
        )
        sys.stdout.write(f"{cf_output}\n")


def _validate_from_args(args: argparse.Namespace) -> None:
    if codicefiscale.is_valid(args.code):
        sys.stdout.write("✅\n")
    else:
        sys.stdout.write("❌\n")


def run() -> None:
    parser = argparse.ArgumentParser(
        description=__description__,
    )
    parser.add_argument(
        "--version",
        required=False,
        action="store_true",
        help="Show library version",
    )

    subparsers = parser.add_subparsers(
        title="subcommands",
        dest="subcommand",
        description="Choose a command",
        required=False,
    )

    decode_parser = subparsers.add_parser(
        "decode",
        help=(
            "Decode an italian Codice Fiscale. "
            "For more info run: 'python -m codicefiscale decode --help'"
        ),
    )
    decode_parser.add_argument(
        "code",
        help="Codice Fiscale to decode",
    )
    decode_parser.add_argument(
        "--omocodes",
        required=False,
        action="store_true",
        help="Include omocodes list",
    )

    encode_parser = subparsers.add_parser(
        "encode",
        help=(
            "Encode an italian Codice Fiscale. "
            "For more info run: 'python -m codicefiscale encode --help'"
        ),
    )
    encode_parser.add_argument(
        "--firstname",
        required=True,
        help="First name",
    )
    encode_parser.add_argument(
        "--lastname",
        required=True,
        help="Last name",
    )
    encode_parser.add_argument(
        "--gender",
        choices=["m", "M", "f", "F"],
        required=True,
        help="Gender (M/F)",
    )
    encode_parser.add_argument(
        "--birthdate",
        required=True,
        help="Date of birth (DD/MM/YYYY)",
    )
    encode_parser.add_argument(
        "--birthplace",
        required=True,
        help="Place of birth (city, province)",
    )

    validate_parser = subparsers.add_parser(
        "validate",
        help=(
            "Validate an italian Codice Fiscale. "
            "For more info run: 'python -m codicefiscale validate --help'"
        ),
    )
    validate_parser.add_argument(
        "code",
        help="Codice Fiscale to validate",
    )

    args = parser.parse_args()
    run_with_args(args)


def run_with_args(args: argparse.Namespace) -> None:
    if args.subcommand is None and args.version:
        sys.stdout.write(f"{__version__}\n")
    elif args.subcommand == "decode":
        _decode_from_args(args)
    elif args.subcommand == "encode":
        _encode_from_args(args)
    elif args.subcommand == "validate":
        _validate_from_args(args)
    else:
        sys.stdout.write("For more info run: 'python -m codicefiscale --help'\n")
