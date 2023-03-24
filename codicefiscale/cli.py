import argparse
import json
import sys
from datetime import datetime
from typing import Any

from codicefiscale import codicefiscale


def _encode_from_args(args: argparse.Namespace) -> None:
    cf = codicefiscale.encode(
        surname=args.lastname,
        name=args.firstname,
        sex=args.gender,
        birthdate=args.birthdate,
        birthplace=args.birthplace,
    )
    sys.stdout.write(f"{cf}\n")


def _decode_from_args(args: argparse.Namespace) -> None:
    cf_data = codicefiscale.decode(args.codicefiscale)
    if not args.omocodes:
        cf_data.pop("omocodes", None)

    def default_encoder(obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, set):
            return list(obj)
        return str(obj)

    cf_output = json.dumps(cf_data, default=default_encoder, indent=4)
    sys.stdout.write(f"{cf_output}\n")


def run() -> None:
    parser = argparse.ArgumentParser(description="Codice Fiscale Encoder/Decoder")
    subparsers = parser.add_subparsers(
        title="subcommands",
        dest="subcommand",
        description="Choose a command",
        required=True,
    )

    encode_parser = subparsers.add_parser(
        "encode",
        help=(
            "Encode an italian Codice Fiscale using the given parameters, "
            "for more info run: python codicefiscale encode --help"
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

    decode_parser = subparsers.add_parser(
        "decode",
        help=(
            "Decode an italian Codice Fiscale, "
            "for more info run: python codicefiscale decode --help"
        ),
    )
    decode_parser.add_argument(
        "codicefiscale",
        help="Codice fiscale to decode",
    )
    decode_parser.add_argument(
        "--omocodes",
        required=False,
        action="store_true",
        help="Include omocodes list",
    )

    args = parser.parse_args()
    run_with_args(args)


def run_with_args(args: argparse.Namespace) -> None:
    if args.subcommand == "encode":
        _encode_from_args(args)
    elif args.subcommand == "decode":
        _decode_from_args(args)
