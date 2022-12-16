import fsutil
from benedict import benedict
from slugify import slugify


def _expect_keys(d, keys):
    assert all(
        [key in d for key in keys]
    ), f"Invalid keys {list(d.keys())}, missing one or more expected keys {keys}."


def _slugify_names(*names):
    return sorted(set(filter(bool, [slugify(name) for name in names])))


def _update_countries_data():
    # https://www.anagrafenazionale.interno.it/area-tecnica/tabelle-di-decodifica/
    data_url = "https://www.anagrafenazionale.interno.it/wp-content/uploads/2022/10/tabella_2_statiesteri.xlsx"
    data = benedict.from_xls(data_url)
    data.standardize()
    # print(data.dump())

    def map_item(item):
        if not item:
            return None

        _expect_keys(
            item,
            [
                "codat" "denominazione",
                "denominazioneistat",
                "denominazioneistat_en",
                "datainiziovalidita",
                "datafinevalidita",
            ],
        )

        code = item.get_str("codat").upper()
        if not code:
            return None
        assert len(code) == 4, f"Invalid code: '{code}'"

        name = item.get_str("denominazione").title()
        assert name != "", f"Invalid name: '{name}'"
        name_alt = item.get_str("denominazioneistat").title()
        name_alt_en = item.get_str("denominazioneistat_en").title()
        name_slugs = _slugify_names(name, name_alt, name_alt_en)

        province = "EE"

        date_created = item.get_datetime("datainiziovalidita")
        date_deleted = item.get_datetime("datafinevalidita")
        date_deleted_raw = item.get_str("datafinevalidita")
        if "9999" in date_deleted_raw:
            date_deleted = ""

        return {
            "active": False if date_deleted else True,
            "code": code,
            "date_created": date_created,
            "date_deleted": date_deleted,
            "name": name,
            "name_alt": name_alt,
            "name_alt_en": name_alt_en,
            "name_slugs": name_slugs,
            "province": province,
        }

    _write_data_json(
        filepath="../codicefiscale/data/countries.json",
        data=[map_item(benedict(item)) for item in data["values"]],
    )


def _update_municipalities_data():
    # https://www.anagrafenazionale.interno.it/area-tecnica/tabelle-di-decodifica/
    data_url = "https://www.anagrafenazionale.interno.it/wp-content/uploads/2022/12/ANPR_archivio_comuni.csv"
    data = benedict.from_csv(data_url)
    data.standardize()

    def map_item(item):
        if not item:
            return None

        _expect_keys(
            item,
            [
                "stato",
                "codcatastale",
                "denominazione_it",
                "denomtraslitterata",
                "altradenominazione",
                "altradenomtraslitterata",
                "siglaprovincia",
                "dataistituzione",
                "datacessazione",
            ],
        )

        status = item.get("stato", "").upper()
        assert len(status) == 1 and status in ["A", "C"], f"Invalid status: '{status}'"
        active = status == "A"

        code = item.get_str("codcatastale").upper()
        assert code == "ND" or len(code) == 4, f"Invalid code: '{code}'"

        name = item.get_str("denominazione_it").title()
        assert name != "", f"Invalid name: {name}"

        name_trans = item.get_str("denomtraslitterata").title()
        name_alt = item.get_str("altradenominazione").title()
        name_alt_trans = item.get_str("altradenomtraslitterata").title()
        name_slugs = _slugify_names(name, name_trans, name_alt, name_alt_trans)

        province = item.get("siglaprovincia", "").upper()
        assert len(province) == 2, f"Invalid province: '{province}'"

        date_created = item.get_datetime("dataistituzione")
        date_deleted = item.get_datetime("datacessazione")
        date_deleted_raw = item.get_str("datacessazione")
        if "9999" in date_deleted_raw:
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

    _write_data_json(
        filepath="../codicefiscale/data/municipalities.json",
        data=[map_item(benedict(item)) for item in data["values"]],
    )


def _write_data_json(filepath, data):
    data = list(filter(bool, data))
    data = sorted(data, key=lambda item: item["name"])
    data_filepath = fsutil.join_path(__file__, filepath)
    fsutil.write_file_json(data_filepath, data, indent=4, sort_keys=True)


def main():
    _update_countries_data()
    _update_municipalities_data()


if __name__ == "__main__":
    main()
