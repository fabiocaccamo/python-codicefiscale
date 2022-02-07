# -*- coding: utf-8 -*-

from benedict import benedict
from slugify import slugify

import fsutil


def _update_municipalities_data():

    data_url = "https://www.anagrafenazionale.interno.it/wp-content/uploads/ANPR_archivio_comuni.csv"
    data = benedict.from_csv(data_url)
    data.standardize()

    def map_item(item):

        status = item.get("stato", "").upper()
        assert len(status) == 1 and status in ["A", "C"]
        active = status == "A"

        code = item.get_str("codcatastale").upper()
        assert code == "ND" or len(code) == 4, f"Invalid code: {code}"

        name = item.get_str("denominazione_it").title()
        assert name != "", f"Invalid name: {name}"

        name_trans = item.get_str("denomtraslitterata").title()
        name_alt = item.get_str("altradenominazione").title()
        name_alt_trans = item.get_str("altradenomtraslitterata").title()
        name_slugs = sorted(
            set(
                filter(
                    bool,
                    [
                        slugify(name),
                        slugify(name_trans),
                        slugify(name_alt),
                        slugify(name_alt_trans),
                    ],
                )
            )
        )
        province = item.get("siglaprovincia", "").upper()
        assert len(province) == 2, f"Invalid province: {province}"

        date_created = item.get_str("dataistituzione")
        date_deleted = item.get_str("datacessazione")
        if date_deleted.startswith("9999"):
            date_deleted = ""

        return {
            "active": active,
            "code": code,
            "date_created": date_created,
            "date_deleted": date_deleted,
            "name": name,
            "name_trans": name_trans,
            "name_alt": name_alt,
            "name_alt_trans": name_alt_trans,
            "name_slugs": name_slugs,
            "province": province,
        }

    output_data = [map_item(benedict(item)) for item in data["values"]]
    output_path = "../codicefiscale/data/municipalities.json"
    output_abspath = fsutil.join_path(__file__, output_path)
    fsutil.write_file_json(output_abspath, output_data, indent=4)


def main():
    _update_municipalities_data()


if __name__ == "__main__":
    main()
