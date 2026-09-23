import xml.etree.ElementTree as ET

from ers_dpkeys_comparator import compare_ers_dpkeys


def build_root(keys):
    """
    keys: list of (key_attrib_dict, [dk_attrib_dict, ...])
    Builds a ROOT/KEYS/KEY/DK tree matching the ERS DPKeys XML shape.
    """
    root = ET.Element("ROOT")
    keys_el = ET.SubElement(root, "KEYS")

    for key_attrib, dks in keys:
        key_el = ET.SubElement(keys_el, "KEY", key_attrib)
        for dk_attrib in dks:
            ET.SubElement(key_el, "DK", dk_attrib)

    return root


def test_missing_dk_is_reported():
    cb_root = build_root([
        ({"c": "K1", "v": "10"}, [{"id": "1", "v": "5"}]),
    ])
    ac_root = build_root([
        ({"c": "K1", "v": "10"}, []),
    ])

    _, _, missing_records, _ = compare_ers_dpkeys(cb_root, ac_root)

    assert missing_records == [
        {"Type": "DK", "Key": "K1", "DK ID": "1", "Details": "DK missing in AC"}
    ]


def test_ac_zero_value_dk_is_ignored():
    cb_root = build_root([
        ({"c": "K1", "v": "10"}, [{"id": "1", "v": "5"}]),
    ])
    ac_root = build_root([
        ({"c": "K1", "v": "10"}, [
            {"id": "1", "v": "5"},
            {"id": "2", "v": "0.0"},
        ]),
    ])

    differences, zero_values, missing_records, duplicate_records = compare_ers_dpkeys(
        cb_root, ac_root
    )

    # The extra AC-only DK (id=2) is zero, so it must be ignored entirely,
    # not reported as "missing in CB".
    assert differences == []
    assert zero_values == []
    assert missing_records == []
    assert duplicate_records == []


def test_duplicate_dk_detected():
    cb_root = build_root([
        ({"c": "K1", "v": "10"}, [
            {"id": "1", "v": "5"},
            {"id": "1", "v": "5"},
        ]),
    ])
    ac_root = build_root([
        ({"c": "K1", "v": "10"}, [{"id": "1", "v": "5"}]),
    ])

    _, _, _, duplicate_records = compare_ers_dpkeys(cb_root, ac_root)

    assert duplicate_records == [
        {
            "Type": "DK",
            "Key": "K1",
            "DK ID": "1",
            "Details": "Duplicate DK found in CB",
        }
    ]


def test_key_level_value_difference_reported():
    cb_root = build_root([
        ({"c": "K1", "v": "100"}, []),
    ])
    ac_root = build_root([
        ({"c": "K1", "v": "200"}, []),
    ])

    differences, _, _, _ = compare_ers_dpkeys(cb_root, ac_root)

    assert differences == [
        {"Type": "KEY", "Key": "K1", "Field": "v", "CB Value": "100", "AC Value": "200"}
    ]


def test_full_comparison_returns_expected_result():
    cb_root = build_root([
        ({"c": "K1", "v": "100"}, [
            {"id": "1", "v": "62.9000"},
            {"id": "2", "v": "10"},
        ]),
        ({"c": "K2", "v": "50"}, [
            {"id": "1", "v": "5"},
        ]),
    ])
    ac_root = build_root([
        ({"c": "K1", "v": "100"}, [
            {"id": "1", "v": "62.9"},
            {"id": "2", "v": "9.5"},
            {"id": "3", "v": "0.0"},
        ]),
    ])

    differences, zero_values, missing_records, duplicate_records = compare_ers_dpkeys(
        cb_root, ac_root
    )

    assert zero_values == []
    assert duplicate_records == []
    assert differences == [
        {
            "Type": "DK",
            "Key": "K1",
            "DK ID": "2",
            "Field": "v",
            "CB Value": "10",
            "AC Value": "9.5",
        }
    ]
    assert missing_records == [
        {"Type": "KEY", "Key": "K2", "Details": "KEY missing in AC"}
    ]
