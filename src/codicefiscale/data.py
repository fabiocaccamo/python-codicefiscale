from __future__ import annotations

import os
import sys
from datetime import datetime
from typing import Any

import fsutil


def get_data_basedir() -> str:
    if getattr(sys, "frozen", False):
        # standalone executable (eg. PyInstaller)
        return os.path.dirname(sys.executable)
    return __file__


def get_data(filename: str) -> Any:
    return fsutil.read_file_json(
        fsutil.join_path(get_data_basedir(), f"data/{filename}")
    )


def get_municipalities_data() -> Any:
    municipalities = get_data("municipalities.json")
    return municipalities


def get_countries_data() -> Any:
    deleted_countries = get_data("deleted-countries.json")
    countries = get_data("countries.json")
    return deleted_countries + countries


def get_indexed_data() -> dict[
    str, dict[str, list[dict[str, bool | datetime | str | list[str]]]]
]:
    municipalities = get_municipalities_data()
    countries = get_countries_data()
    data: dict[str, dict[str, list[dict[str, bool | datetime | str | list[str]]]]] = {
        "municipalities": {},
        "countries": {},
        "codes": {},
    }

    for municipality in municipalities:
        code = municipality["code"]
        province = municipality["province"].lower()
        names = municipality["name_slugs"]
        for name in names:
            name_and_province = f"{name}-{province}"
            data["municipalities"].setdefault(name, [])
            data["municipalities"].setdefault(name_and_province, [])
            data["municipalities"][name].append(municipality)
            data["municipalities"][name_and_province].append(municipality)
        data["codes"].setdefault(code, [])
        data["codes"][code].append(municipality)

    for country in countries:
        code = country["code"]
        names = country["name_slugs"]
        for name in names:
            data["countries"].setdefault(name, [])
            data["countries"][name].append(country)
        data["codes"].setdefault(code, [])
        data["codes"][code].append(country)

    return data
