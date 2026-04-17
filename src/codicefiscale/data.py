from __future__ import annotations

import os
import sys
from typing import Any

import fsutil
from slugify import slugify


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


def get_names_data() -> Any:
    names = get_data("names.json")
    return names


def get_indexed_data() -> dict[str, Any]:
    from codicefiscale.codicefiscale import encode_firstname

    municipalities = get_municipalities_data()
    countries = get_countries_data()
    names = get_names_data()

    data: dict[str, Any] = {
        "municipalities": {},
        "countries": {},
        "codes": {},
        "names": {},
    }

    for municipality in municipalities:
        code = municipality["code"]
        province = municipality["province"].lower()
        municipality_unicode_slug = slugify(municipality["name"], allow_unicode=True)
        municipality_names = [municipality_unicode_slug] + municipality["name_slugs"]
        for name in municipality_names:
            name_and_province = f"{name}-{province}"
            data["municipalities"].setdefault(name, [])
            data["municipalities"].setdefault(name_and_province, [])
            data["municipalities"][name].append(municipality)
            data["municipalities"][name_and_province].append(municipality)
        data["codes"].setdefault(code, [])
        data["codes"][code].append(municipality)

    for country in countries:
        code = country["code"]
        country_names = country["name_slugs"]
        for name in country_names:
            data["countries"].setdefault(name, [])
            data["countries"][name].append(country)
        data["codes"].setdefault(code, [])
        data["codes"][code].append(country)

    for gender, gender_names in names.items():
        for name in gender_names:
            code = encode_firstname(name)
            data["names"].setdefault(code, {"M": set(), "F": set()})
            data["names"][code][gender].add(name)

    for code in data["names"]:
        data["names"][code]["M"] = sorted(data["names"][code]["M"])
        data["names"][code]["F"] = sorted(data["names"][code]["F"])

    return data
